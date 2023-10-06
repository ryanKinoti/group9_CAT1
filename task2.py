import os
import os.path
import json
from typing import List
from logs_settings import *


def fetch_and_prepare_dataset(project_folder: str) -> str:
    data_folder = os.path.join(project_folder, '1.1')

    languages_to_fetch = ['en-US', 'sw-KE', 'de-DE']

    selected_files = []

    for lang in languages_to_fetch:
        file_path = os.path.join(data_folder, f'{lang}.jsonl')
        if os.path.isfile(file_path):
            selected_files.append(file_path)
        else:
            logging.warning(f"{lang}.jsonl file not found in the specified path: {file_path}")

    if not selected_files:
        raise ValueError("No files found for the specified languages.")

    return selected_files


def generate_jsonl_files_for_languages(path_to_data: str, languages: List[str], destination_folder: str,) -> None:
    """
    Generates separate JSONL files for specified languages
    :param path_to_data: path to where the jsonl files have been downloaded
    :param languages: list of languages for which to generate JSONL files
    :param destination_folder: folder where the resulting jsonl files will be stored
    :return:
    """

    for lang in languages:
        lang_file_path = os.path.join(path_to_data, f"{lang}.jsonl")
        if os.path.isfile(lang_file_path):
            with open(lang_file_path, "r", encoding='utf-8') as lang_file:
                lang_data = [json.loads(line) for line in lang_file]

            for split in ['train', 'test', 'dev']:
                split_data = [instruction for instruction in lang_data if instruction.get("partition") == split]

                if split_data:
                    output_file_path = os.path.join(destination_folder, f"{lang}_{split}.jsonl")

                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                    if os.path.isfile(output_file_path):
                        logging.warning(
                            f"{lang}_{split}.jsonl file already exists in the specified output folder: {output_file_path}. Skipping.")
                    else:
                        with open(output_file_path, "w", encoding='utf-8') as output_file:
                            for instruction in split_data:
                                output_file.write(json.dumps(instruction) + '\n')
                else:
                    logging.warning(f"No data found for {lang}_{split}. Skipping.")
        else:
            logging.warning(f"{lang}.jsonl file not found in the specified path: {path_to_data}")


def file_exists(file_path):
    """
    Check if a file exists.
    :param file_path: Path to the file.
    :return: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)


def generate_file(data, output_file_path, overwrite=False):
    """
    Generate a file with the given data.
    :param data: List of data to write to the file.
    :param output_file_path: Path to the output file.
    :param overwrite: If True, overwrite the existing file. If False and the file exists, skip generation.
    :return: True if the file is generated, False if the file already exists and overwrite is False.
    """
    if not overwrite and file_exists(output_file_path):
        print(f"File already exists: {output_file_path}. Skipping.")
        return False

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for item in data:
            output_file.write(json.dumps(item) + '\n')

    print(f"File generated: {output_file_path}")
    return True


def process_jsonl_file(input_file, output_dir, language):
    try:
        with open(input_file, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()

            for partition in ['train', 'dev', 'test']:
                data = [line for line in lines if partition in line]

                output_file_name = f'{language}.{partition}_jsonl'
                with open(os.path.join(output_dir, output_file_name), 'w', encoding='utf-8') as output_file:
                    output_file.writelines(data)

        logger.info(f'Successfully processed {input_file} and generated JSONL files in {output_dir}')

    except Exception as e:
        logger.error(f'Error processing {input_file}: {e}')

