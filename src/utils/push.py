import os
from dotenv import load_dotenv
from pushover import Client

load_dotenv()

pushover = Client(
    user_key=os.getenv("PUSHOVER_USERKEY"), api_token=os.getenv("PUSHOVER_APIKEY")
)


def pushover_message(title, msg):
    pushover.send_message(
        title=title,
        message=msg,
    )
