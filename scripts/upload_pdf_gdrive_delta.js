import { readFileSync, writeFileSync, existsSync, readdirSync, createReadStream, mkdirSync } from "fs";
import { resolve, dirname, join } from "path";
import { fileURLToPath } from "url";
import { google } from "googleapis";
import http from "http";
import { exec } from "child_process";
import crypto from "crypto";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Prioritaskan credentials dari knowledge-base, fallback ke fasih-sync-monitoring
const KB_ROOT = resolve(__dirname, "..");
const FASIH_SYNC_DIR = resolve(KB_ROOT, "..", "fasih-sync-monitoring");

const CREDENTIALS_PATH = existsSync(resolve(KB_ROOT, "credentials.json"))
  ? resolve(KB_ROOT, "credentials.json")
  : resolve(FASIH_SYNC_DIR, "credentials.json");

const USER_TOKEN_PATH = resolve(FASIH_SYNC_DIR, "token_user.json");
const GDRIVE_FOLDER_ID = "1GVLa9UVOBJOr-rb62A539HnNK7UGyrXa";
const PDF_DIR = resolve(KB_ROOT, "kegiatan/sensus-ekonomi-2026/2026/sqllab_monitoring/pdf_siap_cetak");
const LINK_MAPPING_FILE = resolve(FASIH_SYNC_DIR, "results", "pdf_gdrive_links.json");

const SCOPES = [
  "https://www.googleapis.com/auth/drive.file",
  "https://www.googleapis.com/auth/drive"
];

function getFileMD5(filePath) {
  const fileBuffer = readFileSync(filePath);
  const hashSum = crypto.createHash("md5");
  hashSum.update(fileBuffer);
  return hashSum.digest("hex");
}

async function getOAuth2Client() {
  if (!existsSync(CREDENTIALS_PATH)) {
    throw new Error(`File credentials.json tidak ditemukan di ${CREDENTIALS_PATH}`);
  }

  const keys = JSON.parse(readFileSync(CREDENTIALS_PATH, "utf-8"));
  const creds = keys.installed || keys.web;

  const oAuth2Client = new google.auth.OAuth2(
    creds.client_id,
    creds.client_secret,
    "http://localhost:8888/oauth2callback"
  );

  if (existsSync(USER_TOKEN_PATH)) {
    const token = JSON.parse(readFileSync(USER_TOKEN_PATH, "utf-8"));
    oAuth2Client.setCredentials(token);
    return oAuth2Client;
  }

  return new Promise((resolveClient, reject) => {
    const authUrl = oAuth2Client.generateAuthUrl({
      access_type: "offline",
      scope: SCOPES,
      prompt: "consent"
    });

    console.log("\n==================================================================");
    console.log("🔑 SILAKAN OTORISASI OTOMATIS BERIKUT (CUKUP 1 KALI SAJA):");
    console.log(authUrl);
    console.log("==================================================================\n");

    const server = http.createServer(async (req, res) => {
      try {
        const reqUrl = new URL(req.url, "http://localhost:8888");
        if (reqUrl.pathname === "/oauth2callback") {
          const code = reqUrl.searchParams.get("code");
          if (!code) {
            res.end("Kode otorisasi tidak ditemukan.");
            return;
          }

          const { tokens } = await oAuth2Client.getToken(code);
          oAuth2Client.setCredentials(tokens);
          writeFileSync(USER_TOKEN_PATH, JSON.stringify(tokens, null, 2));
          console.log("🟢 SUKSES! Token OAuth 2.0 User telah disimpan di token_user.json");

          res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
          res.end(`
            <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
              <h1 style="color: #2e7d32;">✅ Otorisasi Berhasil!</h1>
              <p>Token Google OAuth 2.0 milik Bg Ihza telah tersimpan.</p>
            </div>
          `);

          server.close();
          resolveClient(oAuth2Client);
        }
      } catch (err) {
        res.writeHead(500, { "Content-Type": "text/plain" });
        res.end("Error: " + err.message);
        reject(err);
      }
    });

    server.listen(8888, () => {
      exec(`xdg-open "${authUrl}"`, () => {});
    });
  });
}

export async function uploadPDFsWithDeltaSync() {
  if (!existsSync(PDF_DIR)) {
    console.error(`❌ Folder PDF tidak ditemukan: ${PDF_DIR}`);
    return {};
  }

  const pdfFiles = readdirSync(PDF_DIR).filter(f => f.endsWith(".pdf"));
  if (pdfFiles.length === 0) {
    console.log("⚠️ Tidak ada berkas PDF di folder pdf_siap_cetak.");
    return {};
  }

  console.log(`📌 Memulai Delta Upload ke Google Drive (${pdfFiles.length} PDF lokal)...`);
  const auth = await getOAuth2Client();
  const drive = google.drive({ version: "v3", auth });

  // 1. Dapatkan SELURUH berkas GDrive yang ada menggunakan Pagination (pageToken)
  console.log("🔍 Fetching daftar lengkap berkas di GDrive (dengan Pagination)...");
  const existingMap = new Map();
  let pageToken = null;
  let totalRemoteFiles = 0;

  try {
    do {
      const listRes = await drive.files.list({
        q: `'${GDRIVE_FOLDER_ID}' in parents and trashed = false`,
        fields: "nextPageToken, files(id, name, webViewLink, md5Checksum)",
        pageSize: 1000,
        pageToken: pageToken,
        supportsAllDrives: true,
        includeItemsFromAllDrives: true,
      });

      for (const f of listRes.data.files || []) {
        existingMap.set(f.name, f);
        totalRemoteFiles++;
      }
      pageToken = listRes.data.nextPageToken;
    } while (pageToken);

    console.log(`  ✓ Berhasil mengambil ${totalRemoteFiles} berkas dari GDrive.`);
  } catch (e) {
    console.warn("  ⚠️ Gagal list berkas GDrive:", e.message);
  }

  const linkMapping = loadLinkMappingCache();
  let skippedCount = 0;
  let updatedCount = 0;
  let createdCount = 0;

  for (let i = 0; i < pdfFiles.length; i++) {
    const filename = pdfFiles[i];
    const codeMatch = filename.match(/^(\d{16})/);
    const subslsCode = codeMatch ? codeMatch[1] : null;
    const filePath = join(PDF_DIR, filename);

    try {
      const localMD5 = getFileMD5(filePath);

      if (existingMap.has(filename)) {
        const existingFile = existingMap.get(filename);
        const webViewLink = existingFile.webViewLink || `https://drive.google.com/file/d/${existingFile.id}/view`;

        // Pengecekan Hash MD5 (Delta Upload)
        if (existingFile.md5Checksum && existingFile.md5Checksum === localMD5) {
          if (subslsCode) linkMapping[subslsCode] = webViewLink;
          skippedCount++;
          continue;
        }

        // MD5 berbeda: Update isi file di GDrive secara In-Place (ID & Link tetap sama)
        console.log(`     🔄 [${i+1}/${pdfFiles.length}] Updating file yang berubah: ${filename}...`);
        await drive.files.update({
          fileId: existingFile.id,
          media: {
            mimeType: "application/pdf",
            body: createReadStream(filePath),
          },
          supportsAllDrives: true,
        });

        if (subslsCode) linkMapping[subslsCode] = webViewLink;
        updatedCount++;
        console.log(`       ✓ Updated in-place: ${webViewLink}`);
        continue;
      }

      // Upload file baru
      console.log(`     ↑ [${i+1}/${pdfFiles.length}] Uploading berkas baru: ${filename}...`);
      const fileMetadata = {
        name: filename,
        parents: [GDRIVE_FOLDER_ID],
      };
      const media = {
        mimeType: "application/pdf",
        body: createReadStream(filePath),
      };

      const file = await drive.files.create({
        requestBody: fileMetadata,
        media: media,
        fields: "id, name, webViewLink, md5Checksum",
        supportsAllDrives: true,
      });

      const fileId = file.data.id;
      const webViewLink = file.data.webViewLink || `https://drive.google.com/file/d/${fileId}/view`;

      try {
        await drive.permissions.create({
          fileId: fileId,
          requestBody: { role: "reader", type: "anyone" },
          supportsAllDrives: true,
        });
      } catch (pErr) {
        // ignore permission error
      }

      if (subslsCode) linkMapping[subslsCode] = webViewLink;
      existingMap.set(filename, { id: fileId, name: filename, webViewLink, md5Checksum: file.data.md5Checksum || localMD5 });
      createdCount++;
      console.log(`       ✓ Uploaded: ${webViewLink}`);
    } catch (err) {
      console.error(`       ❌ Gagal upload ${filename}: ${err.message}`);
    }
  }

  saveLinkMappingCache(linkMapping);
  console.log(`\n🟢 SUKSES DELTA UPLOAD! (Skipped/Identik: ${skippedCount}, Updated: ${updatedCount}, Baru: ${createdCount})`);
  console.log(`📌 Total ${Object.keys(linkMapping).length} PDF terhubung ke Google Drive.`);
  return linkMapping;
}

function saveLinkMappingCache(data) {
  const resultsDir = resolve(FASIH_SYNC_DIR, "results");
  if (!existsSync(resultsDir)) {
    mkdirSync(resultsDir, { recursive: true });
  }
  writeFileSync(LINK_MAPPING_FILE, JSON.stringify(data, null, 2));
}

function loadLinkMappingCache() {
  if (existsSync(LINK_MAPPING_FILE)) {
    try {
      return JSON.parse(readFileSync(LINK_MAPPING_FILE, "utf-8"));
    } catch (e) {
      return {};
    }
  }
  return {};
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  uploadPDFsWithDeltaSync().catch(console.error);
}
