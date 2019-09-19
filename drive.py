# -args(up doc)
import json
from os import path, makedirs
from sys import argv
from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

FILE_IDS = {
        'K1DV5.session': '1_lEqQOPrSLNd78KuK7e89sfPA6rWEAfo',
        'mez-data.json': '13mTNhBRW2nZ-eFYdhxqKFA3rPJf3mwDg',
        'index.html': '1seFscEboAxc0Q3pHLw45uTxP3Zcrl58o',
        }

def authorized_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    if path.exists('drive_token.json'):
        with open('drive_token.json') as file:
            info = json.load(file)
        creds = Credentials(
                None,
                info['refresh_token'],
                token_uri=info['token_uri'],
                client_id=info['client_id'],
                client_secret=info['client_secret']
                )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'drive_client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080, access_type='offline')
        # Save the credentials for the next run
        with open('drive_token.json', 'w') as file:
            json.dump({
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                }, file)

    return build('drive', 'v3', credentials=creds)

def download_file(service, file):
    file_id = FILE_IDS[path.basename(file)]
    request = service.files().get_media(fileId=file_id)
    with open(file, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

def update_file(service, file):
    media = MediaFileUpload(file)
    file = service.files().update(media_body=media,  # create for uploading, - fileId + metadata
                                  fileId=FILE_IDS[path.basename(file)]).execute()


if __name__ == '__main__':
    service = authorized_service()
    if len(argv) == 3:
        direction, command = argv[1:]
        # first download and then upload
        if direction == 'down':
            if command == 'bot':
                download_file(service, 'K1DV5.session')
                download_file(service, 'mez-data.json')
            elif command == 'doc':
                download_file(service, 'K1DV5.session')
                download_file(service, 'mez-data.json')
                makedirs('dist', exist_ok=True)
                download_file(service, 'dist/index.html')
        elif direction == 'up':
            if command in ['bot', 'doc']:
                update_file(service, 'mez-data.json')
            elif command == 'template':
                update_file(service, 'dist/index.html')
