import os.path
import os

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


def upload_files(new_drive_folder: str, path: str) -> None:
    """
    Uploads user specified files or folders to google drive
    :param new_drive_folder: Name of the Google Drive folder where the uploads will be stored
    :param path: path to the desired upload
    :return:
    """
    # authentication
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Create new drive folder
    new_folder = create_new_folder(new_drive_folder, drive, 'root')
    parent_id = new_folder['id']

    # Upload files
    upload_function(new_drive_folder, path, drive, parent_id)


def upload_function(new_drive_folder: str, path: str, drive, parent_id: str) -> None:
    """
    Contains actual functionality for the Google Drive upload
    :param new_drive_folder: Name of the Google Drive folder where the uploads will be stored
    :param path: path to the desired upload
    :param drive: an instance of the user's Google Drive connection
    :param parent_id: id denoting the parent file or directory
    :return:
    """
    # if uploading a folder
    if os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            # if uploading a folder of files
            if os.path.isfile(item_path):
                file = drive.CreateFile({
                    'title': item,
                    'parents': [{'id': parent_id}]
                })
                file.Upload()
                print(f'File: {item} successfully uploaded in the folder: {new_drive_folder}')

            # if uploading a folder of folders
            if os.path.isdir(item_path):
                new_folder = create_new_folder(item, drive, parent_id)
                parent_id2 = new_folder['id']
                new_folder2 = new_folder['title']
                upload_function(new_folder2, item_path, drive, parent_id2)

    # if uploading a file
    elif os.path.isfile(path):
        filename = os.path.basename(path)
        file = drive.CreateFile({
            'title': filename,
            'parents': [{'id': parent_id}]
        })
        file.Upload()
        print("Uploading the file - " + f"{filename} to the folder: {new_drive_folder}")

    # if not a file or directory
    else:
        print(f'The specified upload: {path} is neither an existing file nor directory')


def create_new_folder(new_drive_folder: str, drive, parent_id: str):
    """
    Creates a new folder on Google Drive
    :param new_drive_folder:  Name of the Google Drive folder where the uploads will be stored
    :param drive: an instance of the user's Google Drive connection
    :param parent_id: id denoting the parent file or directory
    :return: Returns the name of the created folder
    """
    folder_metadata = {
        'title': new_drive_folder,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_id}]
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    print(f'New folder: {new_drive_folder} successfully created on your drive')
    return folder
