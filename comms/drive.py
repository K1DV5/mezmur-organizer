# -args(up doc)
import json
from os import path
from sys import argv
from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

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

def download_file(service, file_name, file_id):
    request = service.files().get_media(fileId=file_id)
    with open(file_name, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

def update_file(service, file_name, file_id):
    media = MediaFileUpload(file_name)
    # create for uploading, - fileId + metadata
    service.files().update(media_body=media, fileId=file_id).execute()
    print('Updated file "' + file_name + '"')

