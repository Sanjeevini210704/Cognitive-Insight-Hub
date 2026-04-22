import os
from datetime import datetime
from montydb import MontyClient, set_storage

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)

set_storage(repository=DB_DIR, storage="sqlite")
_client = MontyClient(DB_DIR)
db = _client["cogniscan"]

users = db["users"]
analyses = db["analyses"]


def now():
    return datetime.utcnow()
