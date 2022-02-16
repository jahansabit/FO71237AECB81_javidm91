import os
from ntpath import join
import os
from pathlib import Path
from sys import platform

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def joinpath(path="", *args):
    return os.path.join(PROJECT_DIR, path, *args)

########## BOT TOKEN ##########
BOT_TOKEN = "946671094:AAHO4Egu_TsYPaEIy2d389CiDUGMrg0e7-s"
########## BOT TOKEN ##########

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_JSON_FILE_PATH = joinpath("data", "data.json")
