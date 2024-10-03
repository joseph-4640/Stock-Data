import os

# Define model directory (relative or absolute path)
model_directory = os.path.join(os.path.dirname(__file__), "models")

# Or, define it as an environment variable for more flexibility
model_directory = os.getenv('MODEL_DIRECTORY', os.path.join(os.path.dirname(__file__), "models"))
