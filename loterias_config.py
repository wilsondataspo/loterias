from os import environ
from environs import Env

BASE_DIR = environ["PWD"] + "/"

Env.read_env("{}.env".format(BASE_DIR), recurse=False)

class Config:
    TOKEN = environ["TOKEN"]
    URL_LOTO = environ["URL_LOTO"]
    DESTINATION = environ["DESTINATION"]
    