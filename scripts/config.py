import os

# Assuming the project's root directory is the parent of the `scripts` directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw_files', 'dataset2', 'movies_metadata.csv')
