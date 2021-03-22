# KIOT

KIOT is a simple web backend application for managing items within a store. It was created with Python 3.8.2 and designed to be used for MySQL 8.0.23. 
For the design document, see [kiot](https://docs.google.com/document/d/1BMIo-5bP3tBAaxDvO35saMD16hnC48Oa0x8YlFEudhE/edit?usp=sharing).

<!-- GETTING STARTED -->
## Installation

Download the project from github or clone it with git

```bash
git clone https://github.com/Le-Long/REST-API-with-Flask.git
```

It is recommended that you create a virtual environment and activate it first. 

Then use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

You need to change the SQLALCHEMY_DATABASE_URI in file config/production.py to your database URI,
and then create a database named "kiot" for the project.

<!-- USAGE -->
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
<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Charles Le - charles@gotitapp.co

Project Link: [https://github.com/Le-Long/REST-API-with-Flask/tree/master](https://github.com/Le-Long/REST-API-with-Flask/tree/master)