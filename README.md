# Plant Identification App

This Streamlit application allows you to upload an image and try and identify the lant.

## Requirements

- Python 3.8 or higher
- 2GB of free disk space for AI model
- At least 4GB RAM recommended

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/psylsph/plant-id-streamlit
   cd plant-id-streamlit
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   ```

3. Install dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install -y libmagickwand-dev
   pip install -r requirements.txt
   ```

## Usage

### Running the Web Interface

```bash
streamlit run plant-id.py
```
