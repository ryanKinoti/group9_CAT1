import os
import shutil
import requests
from logs_settings import *


def fetch_and_prepare_dataset(project_folder):
    # a check to see if the download and extraction was done
    jsonl_folders = set()
    for root, dirs, files in os.walk(project_folder):
        for file in files:
            if file.endswith(".jsonl"):
                jsonl_folders.add(root)

    if jsonl_folders:
        logger.warning(
            f"The folder(s) {', '.join(jsonl_folders)} already exists and contains .jsonl files. Skipping extraction.")

        jsonl_folders_list = list(jsonl_folders)
        first_folder = jsonl_folders_list[0]
        # logger.info(f'The datasets are in {first_folder}')
        return first_folder
    else:
        try:
            tmp_dir = os.path.join(project_folder, 'tmp')
            os.makedirs(tmp_dir, exist_ok=True)

            logger.info(f'Downloading the Dataset . . . . . .')
            dataset_url = 'https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz'
            response = requests.get(dataset_url)

            with open(os.path.join(tmp_dir, "amazon-massive-dataset-1.1.tar.gz"), "wb") as f:
                f.write(response.content)

            logger.info(f'Unzipping the downloaded Dataset . . . . .')
            shutil.unpack_archive(os.path.join(tmp_dir, "amazon-massive-dataset-1.1.tar.gz"),
                                  extract_dir=project_folder)

            # fetching the dataset folder
            jsonl_folders = set()
            for root, dirs, files in os.walk(project_folder):
                for file in files:
                    if file.endswith(".jsonl"):
                        jsonl_folders.add(root)

            jsonl_folders_list = list(jsonl_folders)
            first_folder = jsonl_folders_list[0]
            logger.info(f'The datasets are in {first_folder}')

            print('\n')

            logger.warning(f'Removing the {tmp_dir} folder')
            os.remove(os.path.join(tmp_dir, "amazon-massive-dataset-1.1.tar.gz"))
            os.rmdir(tmp_dir)
            logger.info(f'Dataset downloading and extraction complete!!')
            return first_folder
        except Exception as e:
            logger.error(f'An error: "{e}" has occurred')
