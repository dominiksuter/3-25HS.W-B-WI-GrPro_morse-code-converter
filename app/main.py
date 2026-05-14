from dotenv import load_dotenv

load_dotenv(override=True)

import os
from db import DatabaseManager
from ui import ViewManager


storage_secret = os.getenv(
    "SSECRET",
    "62ca79c467777fd6101172d11b555bf20608291dc0830ef9e2d66b98346372c2",
)


def start() -> None:
    DatabaseManager.init_db()
    ViewManager(storage_secret=storage_secret, show=False).run()


if __name__ in {"__main__", "__mp_main__"}:
    start()
