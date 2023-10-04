import argparse

from task1 import *
from task2 import *
from google_drive_upload import *
from dataset_loader import *


def main():
    # dataset download and extraction
    project_folder = os.getcwd()
    path_to_data = fetch_and_prepare_dataset(project_folder)

    parser = argparse.ArgumentParser(
        prog='Massive Dataset Manipulator',
        description='What the program does')
    parser.add_argument("--log", help="Enable logging in the known levels", choices=["info", "error", "debug"],
                        dest="log")
    parser.add_argument('-t', "--task", help="Specify the task to run, either 1a (separate xlsx files), 1b (separate "
                                             "xlsx sheets), 1c (specific language) or 2", required=True, dest="task",
                        choices=["1a", '1b', '1c', "2", "upload"])

    parser.add_argument('-ofo', '--output_folder', help='Specify the output folder that will hold all the en-xx.xlsx '
                                                        'files', dest='output_folder')
    parser.add_argument('-ofi', '--output_file', help='Specify the existing output file that will hold the en_xx '
                                                      'sheets', dest='output_file')
    parser.add_argument('-lan', '--language', help='Specify the language for which you would like an en-xx.xlsx file',
                        dest='language')
    parser.add_argument('-ofoc', '--output_folder_c', help='Specify the output folder that will hold the output '
                                                           'en-xx.xlsx file', dest='output_folder_c')
    parser.add_argument('-du', '--desired_upload', help='Specify the path to the file or folder you wish to upload to '
                                                        'google drive', dest='desired_upload')
    parser.add_argument('-df', '--drive_folder', help='Specify the new drive folder you wish to store your upload in',
                        dest='drive_folder')

    parser.add_argument('-output', '--output_jsonl', help='Specify the output folder for generated JSONL files',
                        dest='output_jsonl')

    args = parser.parse_args()

    if args.log:
        # Enable logging
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log)
        logging.basicConfig(level=numeric_level)

    if ((args.task == "1a" and args.output_file)
            or (args.task == "1a" and args.output_folder_c)
            or (args.task == "1a" and args.language)
            or (args.task == "1a" and args.desired_upload)
            or (args.task == "1a" and args.drive_folder)):
        logging.error('This option is not available for task 1a. To proceed with task 1a, kindly specify only your '
                      'desired output folder: -ofo')

    if (args.task == '1a' and args.output_folder) and not (args.output_file or args.language or args.output_folder_c
                                                           or args.desired_upload or args.drive_folder):
        logging.info('Generating the en-xx.xlsx files and storing them in your desired '
                     'output folder: %s ....' % args.output_folder)
        generate_xlsx_files(path_to_data, args.output_folder)

    if args.task == "1a" and not (args.output_folder or args.output_file or args.language or args.output_folder_c
                                  or args.desired_upload or args.drive_folder):
        logging.error('To complete task 1a kindly specify your desired output folder -ofo')

    if ((args.task == "1b" and args.output_folder)
            or (args.task == "1b" and args.output_folder_c)
            or (args.task == "1b" and args.language)
            or (args.task == "1b" and args.desired_upload)
            or (args.task == "1b" and args.drive_folder)):
        logging.error('This option is not available for task 1b. To proceed with task 1b, kindly specify only your '
                      'desired output file: -ofi')

    if args.task == "1b" and not (args.output_folder or args.output_file or args.language or args.output_folder_c or
                                  args.desired_upload or args.drive_folder):
        logging.error('To complete task 1b kindly specify your desired output file -ofi')

    if (args.task == '1b' and args.output_file) and not (
            args.output_folder or args.language or args.output_folder_c or
            args.desired_upload or args.drive_folder):
        logging.info('Generating the en-xx sheets and storing them in your desired '
                     'output file: %s ....' % args.output_file)
        generate_xlsx_sheets(path_to_data, args.output_file)

    if ((args.task == "1c" and args.output_folder) or (args.task == "1c" and args.output_file) or
            (args.task == "1c" and args.desired_upload) or (args.task == "1c" and args.drive_folder)):
        logging.error('This option is not available for task 1c. To proceed with task 1c, kindly specify only your '
                      'desired language: -lan and your desired output_folder: -ofoc')

    if args.task == "1c" and not (args.output_folder or args.output_file or args.language or args.output_folder_c or
                                  args.desired_upload or args.drive_folder):
        logging.error('To complete task 1c kindly specify your desired language: -lan and your output folder: -ofoc')

    if args.task == "1c" and (args.language and not args.output_folder_c):
        logging.error('To complete task 1c please also specify your desired output folder ie task=1c, -lan, -ofoc')

    if args.task == "1c" and (args.output_folder_c and not args.language):
        logging.error('To complete task 1c please also specify your desired language ie task=1c, -lan, -ofoc')

    if ((args.task == '1c' and args.language and args.output_folder_c)
            and not (args.output_file or args.output_folder or args.desired_upload or args.drive_folder)):
        logging.info(f'Generating the en-xx.xlsx file for the language: {args.language}'
                     f' and storing it in your desired output folder: {args.output_folder_c}')
        specific_lang_xlsx_file(path_to_data, args.language, args.output_folder_c)

    if args.task == 'upload' and (args.output_folder or args.output_file or args.language or args.output_folder_c):
        logging.error('This option is not available for the upload function. To proceed with your upload'
                      'kindly specify only you desired upload: -du and your new drive folder: -df')

    if args.task == 'upload' and not (args.output_folder or args.output_file or args.language or args.output_folder_c or
                                      args.desired_upload or args.drive_folder):
        logging.error('To complete your upload kindly specify your desired upload: -du and your new drive folder: -df')

    if args.task == 'upload' and (args.desired_upload and not args.drive_folder):
        logging.error('To complete your upload kindly also specify your drive folder: -df ie task=upload, -du, -df')

    if args.task == 'upload' and (args.drive_folder and not args.desired_upload):
        logging.error('To complete your upload kindly also specify the path to '
                      'your desired upload: du ie task=upload, -du, -df')

    if ((args.task == 'upload' and args.desired_upload and args.drive_folder)
            and not (args.output_file or args.output_folder or args.language or args.output_folder_c)):
        logging.info(f'Uploading the files or folders in path: {args.desired_upload}'
                     f' to the google drive folder: {args.drive_folder}')
        upload_files(args.drive_folder, args.desired_upload)

    if args.task == "2" and args.output_jsonl:
        logging.info(f'Generating separate JSONL files for English, Swahili, and German in the folder: {args.output_jsonl}')
        generate_jsonl_files_for_languages(path_to_data, ['en-US', 'sw-KE', 'de-DE'], args.output_jsonl)


if __name__ == "__main__":
    main()
