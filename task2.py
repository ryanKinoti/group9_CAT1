import json
import os
from typing import List, Dict, Any

import pandas as pd

from logs_settings import *


def process_language_files(input_dir, output_dir):
    try:
        summary_file_path = os.path.join(output_dir, '2.1')
        train_languages_df = []

        with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
            languages = ['en-US', 'sw-KE', 'de-DE']

            for lang in languages:
                input_file_path = os.path.join(input_dir, f'{lang}.jsonl')
                output_language_dir = os.path.join(output_dir, lang)

                if not os.path.exists(output_language_dir):
                    os.makedirs(output_language_dir)

                lang_df: pd.DataFrame = process_language_file(input_file_path, output_language_dir, lang)

                summary_file.write(f'{lang} files processed: {os.path.basename(output_language_dir)}\n')

                # save the train data for task 2
                new_annot = lang.split("-")[0] + "_utt"
                lang_df.rename(columns={"utt": new_annot}, inplace=True)
                lang_df = lang_df[["id", new_annot]]

                train_languages_df.append(lang_df)
        logger.info(f'Successfully processed all languages. Summary written to {summary_file_path}')

        process_task3(train_languages_df)


    except Exception as e:
        logger.error(f'Error processing language files: {e}')


def process_language_file(input_file_name, output_dir, language) -> pd.DataFrame | None:
    try:
        with open(input_file_name, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()

            train_data = [line for line in lines if "train" in line]
            dev_data = [line for line in lines if "dev" in line]
            test_data = [line for line in lines if "test" in line]

            train_file_name = f'{language}.train_jsonl'
            dev_file_name = f'{language}.dev_jsonl'
            test_file_name = f'{language}.test_jsonl'

            with open(os.path.join(output_dir, train_file_name), 'w', encoding='utf-8') as train_output:
                train_output.writelines(train_data)

            with open(os.path.join(output_dir, dev_file_name), 'w', encoding='utf-8') as dev_output:
                dev_output.writelines(dev_data)

            with open(os.path.join(output_dir, test_file_name), 'w', encoding='utf-8') as test_output:
                test_output.writelines(test_data)

            logger.info(f'Successfully processed {input_file_name} and generated jsonl files in {output_dir}')
            # process train data
            df_dict: Dict[str, List[Any]] = {}
            # read the file contents line by line
            for line in train_data:
                # convert it to a python dictionary
                json_load = json.loads(line)
                for (key, value) in json_load.items():
                    if key not in df_dict:
                        df_dict[key] = []
                    df_dict[key].append(value)
            df = pd.DataFrame(df_dict)

            return df

    except Exception as e:
        logger.error(f'Error processing {input_file_name}: {e}')
        return None


def process_task3(languages: List[pd.DataFrame], output_dir: str):
    """
    Generates one large json file showing all the translations from en to xx with id and utt for all the train sets.

    :param languages: English, Swahili and German train sets
    :param output_dir: The output directory to stor it in

    :return: None
    """
    en_train = languages[0]
    sw_train = languages[1]
    de_train = languages[2]

    # we do a database style join on id since there can be id's that don't
    # exist in both datasets, the inner join ensures the id's not in one are dropped

    merged_en_sw = en_train.merge(sw_train, on="id")
    all_merged = merged_en_sw.merge(de_train, on="id")

    all_merged.to_json(f"./{output_dir}/task3.jsonl", orient='records', lines=True, index=False, indent=4,
                       force_ascii=False, )
