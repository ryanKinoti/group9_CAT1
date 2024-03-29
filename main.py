import argparse
import sys

from task1 import *
from task2 import *
from google_drive_upload import *
from dataset_loader import *

if __name__ == "__main__":
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

    parser.add_argument('-ofo', '--output_folder', help='Specify the output folder for a specific task '
                                                        'files', dest='output_folder')
    parser.add_argument('-ofi', '--output_file', help='Specify the existing output file that will hold the en_xx '
                                                      'sheets', dest='output_file')
    parser.add_argument('-lan', '--language', help='Specify the language for which you would like an en-xx.xlsx file',
                        dest='language')
    parser.add_argument('-du', '--desired_upload', help='Specify the path to the file or folder you wish to upload to '
                                                        'google drive', dest='desired_upload')
    parser.add_argument('-df', '--drive_folder', help='Specify the new drive folder you wish to store your upload in',
                        dest='drive_folder')

    args = parser.parse_args()

    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log)

    if args.task == "1a":
        if not args.output_folder:
            logging.error('For task 1, you need to specify your output folder -ofo')
            sys.exit(1)
        logging.info('Generating the en-xx.xlsx files and storing them in your desired '
                     'output folder: %s ....' % args.output_folder)
        generate_xlsx_files(path_to_data, args.output_folder)

    if args.task == "1b":
        if not args.output_file:
            logging.error('For task 1b, you need to specify your output file -ofi')
            sys.exit(1)
        logging.info("Generating xls sheet and storing it to  %s" % args.output_file)
        generate_xlsx_sheets(path_to_data, args.output_file)
    if args.task == "1c":
        if not args.language and not args.output_folder:
            logging.error(
                'To complete task 1c kindly specify your desired language: -lan and your output folder: -ofo')
            sys.exit(1)

        logging.info(f'Generating the en-xx.xlsx file for the language: {args.language}'
                     f' and storing it in your desired output folder: {args.output_folder}')
        specific_lang_xlsx_file(path_to_data, args.language, args.output_folder)

    if args.task == "upload":
        if not args.desired_upload and not args.drive_folder:
            logging.error(
                "To complete upload, you need to specify -du/--desired_upload for the folder to upload and "
                "--df/--drive_folder for the folder name")
            sys.exit(1)
        logging.info(f'Uploading the files or folders in path: {args.desired_upload}'
                     f' to the google drive folder: {args.drive_folder}')
        upload_files(args.drive_folder, args.desired_upload)

    if args.task == "2":
        if not args.output_folder:
            logging.error("Task 2 requires you to specify your output folder using -ofo/--output-folder flag")
            sys.exit(1)

        languages_to_fetch = ['en-US', 'sw-KE', 'de-DE']

        generate_jsonl_files_for_languages(path_to_data, languages_to_fetch, args.output_folder)
