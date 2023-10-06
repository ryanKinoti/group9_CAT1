import json
import logging
import os
from typing import List, Dict, Any

import pandas as pd

from logs_settings import *


def generate_jsonl_files_for_languages(path_to_data: str, languages: List[str], destination_folder: str, ) -> None:
    lang_train = []
    for lang in languages:
        lang_file_path = os.path.join(path_to_data, f"{lang}.jsonl")
        if os.path.isfile(lang_file_path):
            with open(lang_file_path, "r", encoding='utf-8') as lang_file:
                lang_data = [json.loads(line) for line in lang_file]

            for split in ['train', 'test', 'dev']:
                split_data = [instruction for instruction in lang_data if instruction.get("partition") == split]

                if split == "train":
                    df_dict: Dict[str, List[Any]] = {}
                    for line in lang_data:
                        for (key, value) in line.items():
                            if key not in df_dict:
                                df_dict[key] = []
                            df_dict[key].append(value)
                    df = pd.DataFrame(df_dict)
                    lang_train.append(df)

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
            logging.error(f"{lang}.jsonl file not found in the specified path: {path_to_data}")
            return

    combine_dataframes(lang_train, destination_folder)


def file_exists(file_path):
    return os.path.isfile(file_path)


def generate_file(data, output_file_path, overwrite=False):
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


def combine_dataframes(languages: List[pd.DataFrame], output_dir: str):
    en_train = languages[0]
    sw_train = languages[1]
    de_train = languages[2]
    logging.info("Combining en, sw and de dataframes on id")

    merged_en_sw = en_train.merge(sw_train, on="id")
    all_merged = merged_en_sw.merge(de_train, on="id")

    all_merged.to_json(f"./{output_dir}/task3.jsonl", orient='records', lines=True, index=False, indent=4,
                       force_ascii=False, )
    logging.info("Finished combining data")
