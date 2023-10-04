from dataset_loader import *


def main():
    project_folder = os.getcwd()
    extracted_folder = os.path.join(project_folder, '1.1')

    fetch_and_prepare_dataset(project_folder, extracted_folder)


if __name__ == "__main__":
    main()
