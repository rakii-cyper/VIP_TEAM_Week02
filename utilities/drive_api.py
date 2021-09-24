from __future__ import print_function

import gdown
import os
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools


def download_videos_google_drive(folder_name, dest_path='Videos') -> bool:
    """
    function to download a file from a google drive folder using drive api and gdown library
    :param folder_name: google drive folder name
    :param dest_path: local destination directory to save
    :return: True if success
    """
    # connect to google api
    scopes = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    drive = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    # get folder id
    folder_query = "name = '{}' and mimeType = 'application/vnd.google-apps.folder'".format(folder_name)
    folder_id = drive.files().list(q=folder_query,
                                   spaces='drive',
                                   fields='files(id, name)').execute()
    folder_id = folder_id.get('files', [])[0]
    folder_id = folder_id.get('id')

    # get id of list file in folder
    file_query = "mimeType contains 'video/' and '{}' in parents".format(folder_id)
    files = drive.files().list(q=file_query,
                               spaces='drive',
                               fields='files(id, name)').execute()

    if not os.path.exists('videos'):
        os.mkdir('videos')

    for fi in files.get('files', []):
        url = 'https://drive.google.com/uc?id='
        url += fi.get('id')
        output = os.path.join(dest_path, fi.get('name'))
        gdown.download(url, output, quiet=False)

    return True
