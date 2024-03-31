from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("URL")
port = os.getenv("PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
index_name = "movies"  # Consider moving this to an environment variable if it could change


def get_es_config():
    return {
        "url": url,
        "port": port,
        "username": username,
        "password": password,
        "index_name": index_name,
    }
