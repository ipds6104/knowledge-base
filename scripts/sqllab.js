import { chromium } from "patchright";
import { platform } from "os";
import dns from "dns";
import { config } from "dotenv";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";

const __dirname = dirname(fileURLToPath(import.meta.url));
config({ path: resolve(__dirname, "..", ".env") });
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

const BASE_URL = "https://fasih-dashboard.bps.go.id";
const USERNAME = process.env.FASIH_USERNAME;
const PASSWORD = process.env.FASIH_PASSWORD;

const COOKIES_PATH = resolve(__dirname, "..", "data", "cookies", "fasih-dashboard.json");
const STORAGE_PATH = COOKIES_PATH.replace(".json", "-storage.json");

const ensureDir = (fp) => mkdirSync(dirname(fp), { recursive: true });

async function getChromeArgs() {
  const args = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
    "--ignore-certificate-errors",
    "--ignore-ssl-errors",
    "--allow-insecure-localhost",
    "--window-size=1280,800",
  ];
  const domains = ["fasih-dashboard.bps.go.id", "sso.bps.go.id"];
  const rules = [];
  for (const domain of domains) {
    try {
      const ips = await dns.promises.resolve4(domain);
      if (ips && ips.length > 0) {
        rules.push(`MAP ${domain} ${ips[0]}`);
      }
    } catch (err) {
      console.warn(`  ⚠️ Gagal resolusi DNS lokal untuk ${domain}: ${err.message}`);
    }
  }
  if (rules.length > 0) {
    args.push(`--host-resolver-rules=${rules.join(', ')}`);
  }
  return args;
}

function getCookiePaths(username) {
  const safeName = (username || "default").replace(/[^a-zA-Z0-9_-]/g, "_");
  const cookiesPath = resolve(__dirname, "..", "data", "cookies", `fasih-dashboard-${safeName}.json`);
  const storagePath = cookiesPath.replace(".json", "-storage.json");
  return { cookiesPath, storagePath };
}

// Perform Playwright login and store session
async function performLogin(username, password, cookiesPath, storagePath) {
  console.log(`→ Meluncurkan browser untuk login BPS SSO akun: ${username}...`);
  const chromePath = platform() === "win32"
    ? "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    : "/usr/bin/google-chrome-stable";

  const args = await getChromeArgs();
  const browser = await chromium.launch({
    headless: true,
    executablePath: chromePath,
    args
  });

  const context = await browser.newContext({
    ignoreHTTPSErrors: true,
    locale: "id-ID",
    viewport: { width: 1280, height: 800 },
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  });

  const page = await context.newPage();
  try {
    console.log("→ Menavigasi ke halaman login...");
    await page.goto(`${BASE_URL}/login/`, { waitUntil: "domcontentloaded", timeout: 45000 });
    
    console.log("→ Mengklik tombol login SSO...");
    await page.click("button:has-text('GO!')");
    
    console.log("→ Menunggu pengalihan ke SSO...");
    await page.waitForURL((url) => url.hostname.includes("sso.bps.go.id"), { timeout: 30000 });
    
    console.log("→ Mengisi kredensial SSO...");
    await page.waitForSelector("#username", { timeout: 15000 });
    await page.fill("#username", username);
    await page.fill("#password", password);
    await page.click("#kc-login");
    
    console.log("→ Menunggu kembali ke dashboard...");
    await page.waitForURL((url) => url.hostname.includes("fasih-dashboard.bps.go.id"), { timeout: 30000 });
    
    console.log("→ Mendapatkan token CSRF dari halaman SQLLab...");
    await page.goto(`${BASE_URL}/superset/sqllab/`, { waitUntil: "domcontentloaded", timeout: 45000 });
    
    const csrfToken = await page.evaluate(() => {
      const el = document.getElementById("csrf_token");
      return el ? el.value : null;
    });

    if (!csrfToken) {
      throw new Error("Gagal mengekstrak CSRF token dari halaman SQLLab");
    }

    const cookies = await context.cookies();
    ensureDir(cookiesPath);
    writeFileSync(cookiesPath, JSON.stringify(cookies, null, 2));
    const storageState = await context.storageState();
    writeFileSync(storagePath, JSON.stringify(storageState, null, 2));

    console.log(`✓ Login berhasil! Cookie dan Token CSRF telah disimpan (${cookiesPath}).`);
    return { cookies, csrfToken };
  } finally {
    await browser.close();
  }
}

// Retrieve active CSRF token
async function getCsrfTokenFromPage(storagePath, cookiesPath) {
  const chromePath = platform() === "win32"
    ? "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    : "/usr/bin/google-chrome-stable";

  const args = await getChromeArgs();
  const browser = await chromium.launch({
    headless: true,
    executablePath: chromePath,
    args
  });

  const context = await browser.newContext({
    storageState: storagePath,
    ignoreHTTPSErrors: true,
    locale: "id-ID",
    viewport: { width: 1280, height: 800 },
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  });

  const page = await context.newPage();
  try {
    await page.goto(`${BASE_URL}/superset/sqllab/`, { waitUntil: "domcontentloaded", timeout: 30000 });
    
    if (page.url().includes("/login/")) {
      return null;
    }

    const csrfToken = await page.evaluate(() => {
      const el = document.getElementById("csrf_token");
      return el ? el.value : null;
    });

    if (csrfToken && cookiesPath) {
      const cookies = await context.cookies();
      writeFileSync(cookiesPath, JSON.stringify(cookies, null, 2));
      const storageState = await context.storageState();
      writeFileSync(storagePath, JSON.stringify(storageState, null, 2));
    }

    return csrfToken;
  } catch (err) {
    return null;
  } finally {
    await browser.close();
  }
}

// Execute query via native fetch with rules checking
async function executeQuery(sql, cookieStr, csrfToken, options = {}) {
  if (sql.includes("SELECT *") || sql.includes("select *")) {
    console.warn("⚠️ PERINGATAN: Superset SQL Lab melarang klausa 'SELECT *'. Harap sebutkan nama kolom secara eksplisit!");
  }

  const randStr = (len = 10) => {
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let res = "";
    for (let i = 0; i < len; i++) {
      res += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return res;
  };

  const payload = {
    client_id: randStr(10),
    database_id: options.databaseId ?? 25,
    json: true,
    runAsync: false,
    schema: options.schema ?? "tgr_fd68e454",
    sql: sql,
    sql_editor_id: options.sqlEditorId ?? "950527",
    tab: options.tab ?? "KB SQLLab Query",
    tmp_table_name: "",
    select_as_cta: false,
    ctas_method: "TABLE",
    queryLimit: options.queryLimit ?? 9000,
    expand_data: true
  };

  const res = await fetch(`${BASE_URL}/api/v1/sqllab/execute/`, {
    method: "POST",
    headers: {
      "accept": "application/json",
      "content-type": "application/json",
      "x-csrftoken": csrfToken || "",
      "cookie": cookieStr,
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    },
    body: JSON.stringify(payload)
  });

  return res;
}

async function run() {
  const args = process.argv.slice(2);
  let sql = "";
  let databaseId = 25;
  let schema = "tgr_fd68e454";
  let queryLimit = 9000;
  let outputFile = null;

  let requestedUser = null;
  let requestedPass = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--db" || args[i] === "--database-id") {
      databaseId = parseInt(args[++i], 10);
    } else if (args[i] === "--schema") {
      schema = args[++i];
    } else if (args[i] === "--limit") {
      queryLimit = parseInt(args[++i], 10);
    } else if (args[i] === "--user" || args[i] === "--username" || args[i] === "--account") {
      requestedUser = args[++i];
    } else if (args[i] === "--pass" || args[i] === "--password") {
      requestedPass = args[++i];
    } else if (args[i] === "--file" || args[i] === "-f") {
      const filePath = resolve(args[++i]);
      sql = readFileSync(filePath, "utf-8");
    } else if (args[i] === "--output" || args[i] === "-o") {
      outputFile = resolve(args[++i]);
    } else if (!sql && !args[i].startsWith("-")) {
      sql = args[i];
    }
  }

  if (!sql) {
    console.error("Penggunaan: node scripts/sqllab.js \"<SQL_QUERY>\" [options]");
    console.error("       atau: node scripts/sqllab.js --file <path/to/query.sql> [options]");
    console.error("Pilihan:");
    console.error("  --db, --database-id <id>    ID database Superset (default: 25 untuk SE2026, 15 untuk Sakernas)");
    console.error("  --schema <schema_name>     Nama schema (default: tgr_fd68e454, Sakernas: tok_3fd42e0e)");
    console.error("  --limit <number>           Batas baris query (default: 9000)");
    console.error("  --account, --user <name>   Username akun FASIH/SSO BPS");
    console.error("  --file, -f <path>          Baca SQL dari berkas");
    console.error("  --output, -o <path>        Simpan output JSON ke berkas");
    process.exit(1);
  }

  // Resolve survey-specific account vs default account
  let username = requestedUser;
  let password = requestedPass;
  const isSakernas = databaseId === 15 || (schema && schema.includes("3fd42e0e"));

  if (!username) {
    if (isSakernas && process.env.FASIH_SAKERNAS_USERNAME) {
      username = process.env.FASIH_SAKERNAS_USERNAME;
      password = process.env.FASIH_SAKERNAS_PASSWORD;
    } else {
      username = process.env.FASIH_USERNAME;
      password = process.env.FASIH_PASSWORD;
    }
  } else if (!password) {
    if (username === process.env.FASIH_SAKERNAS_USERNAME) {
      password = process.env.FASIH_SAKERNAS_PASSWORD;
    } else if (username === process.env.FASIH_USERNAME) {
      password = process.env.FASIH_PASSWORD;
    }
  }

  if (!username || !password) {
    console.error("❌ Kredensial FASIH_USERNAME dan FASIH_PASSWORD harus diset di file .env atau via CLI (--user & --pass)");
    process.exit(1);
  }

  const { cookiesPath, storagePath } = getCookiePaths(username);
  const queryOptions = { databaseId, schema, queryLimit };

  let cookies = [];
  let csrfToken = null;

  if (existsSync(cookiesPath) && existsSync(storagePath)) {
    console.log(`→ Memuat sesi tersimpan untuk ${username}...`);
    try {
      cookies = JSON.parse(readFileSync(cookiesPath, "utf-8"));
      csrfToken = await getCsrfTokenFromPage(storagePath, cookiesPath);
      if (csrfToken) {
        cookies = JSON.parse(readFileSync(cookiesPath, "utf-8"));
      } else {
        console.warn("⚠️ Sesi tersimpan kedaluwarsa.");
      }
    } catch (err) {
      console.warn("⚠️ Gagal memuat sesi:", err.message);
    }
  }

  if (!csrfToken) {
    const fresh = await performLogin(username, password, cookiesPath, storagePath);
    cookies = fresh.cookies;
    csrfToken = fresh.csrfToken;
  }

  const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  console.log(`→ Mengeksekusi query SQL (Akun: ${username}, DB: ${databaseId}, Schema: ${schema}, Limit: ${queryLimit})...`);
  let res = await executeQuery(sql, cookieStr, csrfToken, queryOptions);

  const isUnauthorized = res.status === 401 || res.status === 403;
  let isCsrfMissing = false;
  if (!res.ok) {
    const text = await res.clone().text();
    if (text.includes("CSRF token is missing") || text.includes("CSRF")) {
      isCsrfMissing = true;
    }
  }

  if (isUnauthorized || isCsrfMissing) {
    console.warn(`⚠️ Sesi ditolak (Status ${res.status} atau CSRF kedaluwarsa). Melakukan re-login...`);
    const fresh = await performLogin(username, password, cookiesPath, storagePath);
    const freshCookieStr = fresh.cookies.map(c => `${c.name}=${c.value}`).join('; ');
    res = await executeQuery(sql, freshCookieStr, fresh.csrfToken, queryOptions);
  }

  if (!res.ok) {
    const errorText = await res.text();
    console.error(`❌ Eksekusi gagal (HTTP ${res.status}):`);
    console.error(errorText);
    process.exit(1);
  }

  const result = await res.json();
  if (result.status === "success" && result.data) {
    console.log("🟢 SQL Query berhasil dieksekusi!");
    if (outputFile) {
      ensureDir(outputFile);
      writeFileSync(outputFile, JSON.stringify(result.data, null, 2), "utf-8");
      console.log(`✓ Hasil query berhasil disimpan ke: ${outputFile} (${result.data.length} baris)`);
    } else {
      console.log(JSON.stringify(result.data, null, 2));
    }
  } else {
    console.error("❌ SQL Query gagal dieksekusi oleh Database Engine:");
    console.error(JSON.stringify(result, null, 2));
    process.exit(1);
  }
}

run().catch(err => {
  console.error("❌ Exception terdeteksi:", err.message);
  process.exit(1);
});
