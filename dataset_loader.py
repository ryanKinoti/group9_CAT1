import os
import shutil
import json
import logging
import requests
from logs_settings import *


def fetch_and_prepare_dataset(project_folder, extracted_folder):
    # a check to see if the extraction was done
    if os.path.exists(extracted_folder):
        logger.warning(f"The folder {extracted_folder} already exists. Skipping extraction.")
    else:
        try:
            tmp_dir = os.path.join(project_folder, 'tmp')
            os.makedirs(tmp_dir, exist_ok=True)

            # downloading the dataset
            logger.info(f'Downloading the Dataset')
            dataset_url = 'https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz'
            response = requests.get(dataset_url)

            with open(os.path.join(tmp_dir, "amazon-massive-dataset-1.1.tar.gz"), "wb") as f:
                f.write(response.content)

            logger.info(f'Unzipping the downloaded Dataset')
            shutil.unpack_archive(os.path.join(tmp_dir, "amazon-massive-dataset-1.1.tar.gz"),
                                  extract_dir=project_folder)

            # get the path of the extracted dataset i.e. where the jsonl files are located
            jsonl_files = []
            for root, dirs, files in os.walk(project_folder):
                for file in files:
                    if file.endswith(".jsonl"):
                        print(os.path.join(root, file))

            logger.warning(f'Removing the {tmp_dir} folder')
            os.remove(os.path.join(tmp_dir, "amazon-massive-dataset-1.1.tar.gz"))
            os.rmdir(tmp_dir)

            logger.info(f'Dataset downloading and extraction complete')
        except Exception as e:
            logger.error(f'An error: "{e}" has occurred')
