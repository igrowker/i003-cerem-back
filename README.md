# Api Cerem
## Prerequisites
- **Python 3.8+** (Check with `python3 --version` or `python --version`)
- **pip** (Check with `pip --version`)
- **venv** (Python's built-in virtual environment tool)

If any of these are missing, install them:

### Ubuntu:

- Install Python, pip, and venv:

    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv
    ```

### 2. Create and activate the virtual environment
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```


### 3. Install dependencies
Once the virtual environment is activated, install the required dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```
### 3. Run the server
	python3 site_app/manage.py runserver
	python3 site_app/manage.py runserver
