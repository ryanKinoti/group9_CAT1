# Massive Dataset Translation Project

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Question 1: Generating en-xx.xlsx Files](#usage)
  - [Question 2: Working with Files](#question-2-working-with-files)
- [Contribution](#contribution)


## Introduction

Language translation datasets play a crucial role in advancing natural language processing and machine learning research. This project focuses on harnessing the power of the MASSIVE Dataset to create comprehensive translation datasets. The dataset contains translations from a pivot language (English) to various target languages. With this project, you can effortlessly set up your Python3 development environment, generate language-specific files, and access the generated data for your research and experimentation.

## Prerequisites
Before you get started, make sure you have the following requirements in place:

1. **Integrated Development Environment (IDE)**: Use any Python IDE of your choice. The recommended IDE is PyCharm. You can download it from [Python.org](https://www.jetbrains.com/pycharm/download/?section=windows).

1. **Python 3**:  You will need a Python 3 interpreter to run the scripts. You can download Python 3 from the official website: [Python.org](https://www.python.org/downloads/). Download the latest version of python.

2. **Python Libraries**: The project relies on certain Python libraries. You can install these libraries using the Python package manager, pip:

   - pandas: A powerful data manipulation and analysis library
   - json: A library for handling JSON (JavaScript Object Notation) data.
   - openpyxl: A library for working with Excel files.
   
   ```bash
   pip install pandas openpyxl json

## Installation

Follow these steps to set up the project on your machine:

### 1. Clone the Repository:

Open your terminal and navigate to the directory where you want to store the project. Then, run the following command to clone the repository:

```bash
git clone https://github.com/your-username/your-project.git
```
### 2.Navigate to the Project Directory:

Change your working directory to the project folder:

```bash
cd your-repo-project-name
```

### 4.Install Dependencies:

Install the required dependencies using pip:

```bash
pip install pandas openpyxl
```

## Usage

### Question 1: Generating en-xx.xlsx Files

To generate en-xx.xlsx files for all languages based on the MASSIVE Dataset, follow these steps:

#### 1.Navigate to the Project Directory:

Ensure you are in the project directory where the Python scripts are located.

### 2.Run the Question 1 Script:

Execute the script for Question 1:

``` bash
question 1_script.py
```
This script will process the dataset and generate en-xx.xlsx files for all languages where English is the pivot language.

### Question 2: Working with Files

In this section, you'll perform various tasks related to working with files as outlined in the assessment questions.

To run the Question 2 Script:
Execute the script for Question 2:

```bash
question 2_script.py
```
This script will perform the following tasks:

Generate separate JSONL files for 'test,' 'train,' and 'dev' datasets for English, Swahili, and German.
Create one large JSON file containing translations from English (en) to other languages (xx) for the 'train' dataset with 'id' and 'utt.'
The JSON structure will be pretty printed for readability.


## Uploading Files

After running the scripts, you can automate the process of uploading the generated files to your Google Drive Backup Folder and commit any changes to your GitHub repository.

### 1. Google Drive Backup Folder:

You can automate the process of uploading the generated files to your Google Drive Backup Folder using the Google Drive API and a Python script. Here are the steps to set up automated file uploads:

#### Step 1: Set up Google Drive API

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project and enable the Google Drive API for it.
3. Generate credentials (OAuth 2.0 client ID) and download the JSON file containing your credentials. This file will be used in the Python script for authentication.

#### Step 2: Python Script

Use a Python script that utilizes the Google Drive API to upload files to your Google Drive Backup Folder. You can find example scripts and documentation in the [Google Drive API documentation](https://developers.google.com/drive).

#### Step 3: Configure the Script

In the Python script, configure the following:

- Authenticate using your OAuth 2.0 client ID credentials JSON file.
- Specify the source directory where your generated files are located.
- Specify the target directory or folder in your Google Drive where you want to upload the files.

#### Step 4: Run the Script

Execute the Python script to automate the upload process.


### 2.GitHub Repository:

Commit and push all changes to the GitHub repository to keep your code and generated files versioned.

## Contribution
If you'd like to contribute code to the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and thoroughly test them.
4. Submit a Pull Request (PR) with a clear description of your changes and their significance.

This project aims to provide a comprehensive solution for handling massive translation datasets while maintaining code quality and documentation standards. Your contributions are welcome and greatly appreciated!

## Authors
This project was a collaborative effort by multiple individuals.
