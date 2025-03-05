import numpy as np
import pandas as pd 
from datetime import datetime
import os


# Generate Timestamp Filepath

def generate_timestamped_filepath(base_dir,filename):
    """
    Generates and returns a new filepath for given 'filename'.  

    Args:
        base_dir (str): Base directory containing versioned files.
        filename (str): Original filename (e.g., 'abc.csv').

    Returns:
        str: Path to the generated versioned file.

    """
    # Get filename without extension (e.g., 'abc' from 'abc.csv')
    base_name,extension = os.path.splitext(filename)
    extension=extension[1:]
    
    # Create subfolder for the CSV exports
    output_dir = os.path.join(base_dir, f"{base_name}_{extension}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"{timestamp}_{base_name}.{extension}")
    
    # Export DataFrame to CSV
    return output_path#df.to_csv(output_path, index=False)

# Fetch latest_timestamp_filepath

def obtain_latest_timestamp_filepath(base_dir, filename):
    """
    Get the latest timestamped version of the specified filename.

    Args:
        base_dir (str): Base directory containing versioned files.
        filename (str): Original filename (e.g., 'abc.csv').

    Returns:
        str: Path to the latest versioned file.

    Raises:
        FileNotFoundError: If no versioned files are found.
    """
    base_name, extension = os.path.splitext(filename)
    extension = extension[1:]  # Remove the dot from the extension

    target_dir = os.path.join(base_dir, f"{base_name}_{extension}")

    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"Directory '{target_dir}' not found for filename '{filename}'")

    files = sorted(os.listdir(target_dir), reverse=True)

    for file in files:
        if file.endswith(filename):
            print(f"Found latest file: {file}")
            return os.path.join(target_dir, file)

    raise FileNotFoundError(f"No versioned '{filename}' files found in '{target_dir}'")

