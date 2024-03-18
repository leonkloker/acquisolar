# AcquiSolar Project - Test Module

## Overview
This module of the AcquiSolar Project is dedicated to testing and improving the sorting, summary and meta-data extraction function. It includes scripts for classification, data for testing, and documentation for easy setup and usage.

## Directory Structure

- `__pycache__`: Compiled Python files for improved loading times.
- `documents`: Test set documents and test-directory structure for sorting.
- `Modular Architecture`: In the future classification.py will be broken up in a modular architecture for better performance and easier maintenance.
- `prompts`: Contains all prompt documents, including the hierarchical prompts modeled after Josh Payn's approach, and the One_Prompt file, which contains the final prompt.
- `accuracy_tracker_v1.csv`: First version of the accuracy tracking file for classified documents.
- `accuracy_tracker_v2.csv`: Second version of the accuracy tracking file with updated classifications.
- `accuracy_tracker_v3.csv`: Third version of the accuracy tracking file, reflecting the latest classification accuracy before it's implementation and finalization in the backend.
- `classification.py`: The Python script used for classifying documents.
- `holdout.json`: Contains the holdout set for testing the classification accuracy.
- `README.md`: This documentation file.
- `requirements.txt`: Lists all Python dependencies required for the module.

## Setup

To set up the Testing & Sorting module, ensure that you have Python 3 installed and run the following command to install dependencies:

```bash 
pip install -r requirements.txt 
```

## Usage
To classify documents, run the classification.py script from the terminal:

python classification.py
