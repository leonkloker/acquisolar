import pandas as pd
import json
from datetime import datetime

def load_expected_classifications(file_path='structured_data/directory_for_frontend.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Assuming 'data' is a list of dictionaries with 'name' and 'classification' keys
        return {item['name']: item['classification'] for item in data}
    except FileNotFoundError:
        print(f"No such file: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return {}
    except TypeError as e:
        print(f"Unexpected data format in {file_path}: {e}")
        return {}



def calculate_accuracy(predictions, expected_classifications):
    """
    Calculates the classification accuracy based on the predicted and expected classifications.

    Parameters:
    - predictions: A dictionary mapping file names to their predicted classifications.
    - expected_classifications: A dictionary mapping file names to their expected classifications.

    Returns:
    - The accuracy of the classifications as a percentage.
    """
    correct = 0
    for file_name, predicted_class in predictions.items():
        if file_name in expected_classifications and expected_classifications[file_name] == predicted_class:
            correct += 1
    total = len(expected_classifications)
    return (correct / total) * 100 if total > 0 else 0



def update_accuracy_tracker(csv_file_path, new_accuracy, date_time=None):
    """
    Updates the accuracy tracker CSV file with a new accuracy measurement.

    Parameters:
    - csv_file_path: The path to the CSV file used for tracking accuracy over time.
    - new_accuracy: The new accuracy measurement to be added.
    - date_time: The datetime for the accuracy measurement. Uses the current datetime if None.
    """
    date_time = date_time or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_row = pd.DataFrame([{'DateTime': date_time, 'Accuracy': new_accuracy}])
    
    try:
        df = pd.read_csv(csv_file_path)
        df = pd.concat([df, new_row], ignore_index=True)
    except FileNotFoundError:
        df = new_row
    
    df.to_csv(csv_file_path, index=False)
    print("Accuracy tracker updated.")


