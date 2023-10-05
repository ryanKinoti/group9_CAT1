import os
from logs_settings import *


def process_language_files(input_dir, output_dir):
    try:
        summary_file_path = os.path.join(output_dir, '2.1')

        with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
            languages = ['en-US', 'sw-KE', 'de-DE']

            for lang in languages:
                input_file_path = os.path.join(input_dir, '1.1', f'{lang}.jsonl')
                output_language_dir = os.path.join(output_dir, lang)

                if not os.path.exists(output_language_dir):
                    os.makedirs(output_language_dir)

                process_language_file(input_file_path, output_language_dir, lang)

                summary_file.write(f'{lang} files processed: {os.path.basename(output_language_dir)}\n')

        logger.info(f'Successfully processed all languages. Summary written to {summary_file_path}')

    except Exception as e:
        logger.error(f'Error processing language files: {e}')


def process_language_file(input_file, output_dir, language):
    try:
        with open(input_file, 'r', encoding='utf-8') as input_file:
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

        logger.info(f'Successfully processed {input_file} and generated jsonl files in {output_dir}')

    except Exception as e:
        logger.error(f'Error processing {input_file}: {e}')
