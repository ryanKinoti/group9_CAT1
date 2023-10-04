from dataset_loader import *


def main():
    # dataset download and extraction
    project_folder = os.getcwd()
    fetch_and_prepare_dataset(project_folder)


if __name__ == "__main__":
    main()
