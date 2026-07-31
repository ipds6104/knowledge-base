import { readFileSync, existsSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { google } from "googleapis";

const __dirname = dirname(fileURLToPath(import.meta.url));
const KB_ROOT = resolve(__dirname, "..");
const FASIH_SYNC_DIR = resolve(KB_ROOT, "..", "fasih-sync-monitoring");

const CREDENTIALS_PATH = resolve(FASIH_SYNC_DIR, "cerdas-486720-7bebb7cc9924.json");
const SPREADSHEET_ID = "1QWwKu8VMg3jwTW6q1SShMBzS10jkBy6Y4wEd7IDWzb0";
const TAB_TITLE = "Ranking SLS Tidak Ditemukan";
const CSV_PATH = resolve(KB_ROOT, "kegiatan/sensus-ekonomi-2026/2026/sqllab_monitoring/csv/subsls_tidak_ditemukan_ranking.csv");
const LINK_MAPPING_FILE = resolve(FASIH_SYNC_DIR, "results", "pdf_gdrive_links.json");

function parseCSVLine(text) {
  const result = [];
  let cell = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (inQuotes && text[i + 1] === '"') {
        cell += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      result.push(cell.trim());
      cell = "";
    } else {
      cell += c;
    }
  }
  result.push(cell.trim());
  return result;
}

export async function pushToGoogleSheetsNow() {
  if (!existsSync(CSV_PATH)) {
    console.error(`❌ File CSV tidak ditemukan di ${CSV_PATH}`);
    return;
  }

  let pdfLinkMap = {};
  if (existsSync(LINK_MAPPING_FILE)) {
    try {
      pdfLinkMap = JSON.parse(readFileSync(LINK_MAPPING_FILE, "utf-8"));
      console.log(`📌 Memuat cache ${Object.keys(pdfLinkMap).length} link PDF GDrive...`);
    } catch (e) {
      console.warn("⚠️ Gagal membaca cache link PDF:", e.message);
    }
  }

  const rawCSV = readFileSync(CSV_PATH, "utf-8");
  const lines = rawCSV.split(/\r?\n/).filter(line => line.trim().length > 0);
  if (lines.length === 0) {
    console.error("❌ File CSV kosong.");
    return;
  }

  const rawRows = lines.map(parseCSVLine);
  const header = rawRows[0];

  let linkColIdx = header.indexOf("Link PDF Siap Cetak");
  if (linkColIdx === -1) {
    header.push("Link PDF Siap Cetak");
    linkColIdx = header.length - 1;
  }

  const codeColIdx = header.indexOf("Kode Sub-SLS");

  let mappedCount = 0;
  const formattedRows = [header];
  for (let i = 1; i < rawRows.length; i++) {
    const row = rawRows[i];
    const code = codeColIdx !== -1 ? row[codeColIdx] : null;
    const gdriveLink = code ? pdfLinkMap[code] : null;

    if (gdriveLink) {
      row[linkColIdx] = `=HYPERLINK("${gdriveLink}"; "📄 Download / Cetak PDF")`;
      mappedCount++;
    } else {
      row[linkColIdx] = "-";
    }
    formattedRows.push(row);
  }

  console.log(`  ✓ ${mappedCount} dari ${rawRows.length - 1} baris berhasil dipasangkan link PDF.`);

  // Update CSV lokal
  const newCSVContent = formattedRows.map(r => r.map(c => `"${c.replace(/"/g, '""')}"`).join(",")).join("\n");
  writeFileSync(CSV_PATH, newCSVContent, "utf-8");

  if (!existsSync(CREDENTIALS_PATH)) {
    console.error(`❌ File credentials tidak ditemukan di ${CREDENTIALS_PATH}`);
    return;
  }

  const auth = new google.auth.GoogleAuth({
    keyFile: CREDENTIALS_PATH,
    scopes: ["https://www.googleapis.com/auth/spreadsheets"],
  });

  const authClient = await auth.getClient();
  const sheets = google.sheets({ version: "v4", auth: authClient });

  console.log(`  → Menulis ${formattedRows.length} baris (beserta Link PDF) ke Google Sheets tab '${TAB_TITLE}'...`);
  await sheets.spreadsheets.values.clear({
    spreadsheetId: SPREADSHEET_ID,
    range: `'${TAB_TITLE}'!A1:Z1500`,
  });

  await sheets.spreadsheets.values.update({
    spreadsheetId: SPREADSHEET_ID,
    range: `'${TAB_TITLE}'!A1`,
    valueInputOption: "USER_ENTERED",
    requestBody: {
      values: formattedRows,
    },
  });

  console.log(`🟢 SUKSES BESAR! Tab '${TAB_TITLE}' di Google Sheets berhasil diperbarui lengkap dengan Link PDF (${mappedCount} link active).`);
}

pushToGoogleSheetsNow().catch(console.error);
