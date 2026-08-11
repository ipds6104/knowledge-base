"""kb/google_drive.py — Google Drive API connections and mirroring operations."""

import hashlib
import mimetypes
import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

def extract_folder_id(url_or_id: str) -> str:
    """Ekstraksi Google Drive Folder ID dari URL atau mengembalikan ID mentah."""
    url_or_id = url_or_id.strip()
    match = re.search(r'folders/([a-zA-Z0-9_-]+)', url_or_id)
    if match:
        return match.group(1)
    return url_or_id

def get_drive_service():
    """Menginisialisasi Drive API service dengan OAuth 2.0."""
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "Berkas 'credentials.json' tidak ditemukan. "
                    "Pastikan Anda telah mengunduh OAuth Credentials dari Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def compute_file_md5(filepath: Path) -> str:
    """Menghitung MD5 checksum dari berkas lokal."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_or_create_gdrive_folder(service, folder_name: str, parent_id: str) -> str:
    """Memeriksa folder di Google Drive. Jika belum ada, buat baru."""
    safe_name = folder_name.replace("'", "\\'")
    query = (
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"name = '{safe_name}' and "
        f"'{parent_id}' in parents and "
        f"trashed = false"
    )
    results = service.files().list(
        q=query,
        fields="files(id, name)",
        pageSize=10
    ).execute()
    files = results.get('files', [])

    if files:
        return files[0]['id']

    # Buat folder baru jika tidak ditemukan
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

def list_gdrive_contents(service, folder_id: str) -> Dict[str, dict]:
    """Mengembalikan pemetaan nama file/folder -> metadata file di Google Drive."""
    contents = {}
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"

    while True:
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType, md5Checksum, size)",
            pageToken=page_token,
            pageSize=1000
        ).execute()

        for item in results.get('files', []):
            contents[item['name']] = item

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return contents

def upload_or_update_file(
    service,
    local_path: Path,
    parent_id: str,
    existing_file: Optional[dict] = None
) -> Tuple[dict, str]:
    """Mengunggah file baru atau memperbarui file lama di Google Drive."""
    from googleapiclient.http import MediaFileUpload

    mime_type, _ = mimetypes.guess_type(str(local_path))
    if mime_type is None:
        mime_type = 'application/octet-stream'

    media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)

    if existing_file:
        file_id = existing_file['id']
        updated_file = service.files().update(
            fileId=file_id,
            media_body=media,
            fields='id, name, md5Checksum, size'
        ).execute()
        return updated_file, 'UPDATE'
    else:
        file_metadata = {
            'name': local_path.name,
            'parents': [parent_id]
        }
        created_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, md5Checksum, size'
        ).execute()
        return created_file, 'CREATE'
