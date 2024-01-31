# SQL schema generator 

Export a Data Model into a PostgreSQL schema to facilitate the generation of the corresponding table in a SQL Database.

# API endpoint 
You need to provide the **subject** and the **data model name** 

To test the API, navigate to: http://localhost:8000/docs

![api](/docs/api.gif)

# Create a Python Virtual Environement 

To create a virtual environment in Python using the `venv` module, the following command can be executed in the terminal:

```shell
python3 -m venv venv
```
To activate a virtual environment named "venv" in the root path, you can use the following command:

```shell
source venv/bin/activate
```

# Run The Project (testing mode):
Once the virtual environment is activated, the Python script can be run using the `poetry run` command. 

For example, to run a script named `main.py`, use:

```shell
python3 main.py
```

# Environment Variables 

To manage Environment Variables in this project, create a file `.env` in which you can define the needed variables that should be private and secrets e.g database credentials, access tokens, etc. For example: 

```yaml
TOKEN=github-personal-access-token
```
Use the library `python-dotenv` to instantiate the env vars in the python modules, for example: 

```python
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access to GitHub - Personal Access Token env variables 
access_token = os.getenv("TOKEN")
```


