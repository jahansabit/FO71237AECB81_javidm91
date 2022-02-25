import os

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def joinpath(path="", *args):
    return os.path.join(PROJECT_DIR, path, *args)

########## TOKENS ##########
BOT_TOKEN = "946671094:AAHO4Egu_TsYPaEIy2d389CiDUGMrg0e7-s"
USER_CHAT_ID = ""
DEBUG_CHAT_ID = ""
########## TOKENS ##########

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_JSON_FILE_PATH = joinpath("data", "data.json")
SENT_MSG_DATA_JSON_FILE_PATH = joinpath("data", "sent_msg_data.json")
TIME_TO_CHECK_PRODUCTS = 60