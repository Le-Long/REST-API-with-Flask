# KIOT

KIOT is a simple web backend application created with Python 3 for managing items within a store.

## Installation

Download the project from github or clone it with git

```bash
git https://github.com/Le-Long/REST-API-with-Flask.git
```

It is recommended that you create a virtual environment and activate it first. 

Then use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

You need to change the SQLALCHEMY_DATABASE_URI in file config/production.py to your database URI.

## Running

Afterward, you can go to the project directory to run

```bash
python app.py
```
The server will start on http://127.0.0.1:5000

## Testing

Change directory to the project and then you can test it with pytest

```bash
pip install pytest
pytest
```
