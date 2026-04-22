import bcrypt
from .db import users, now


def hash_password(pw: str) -> bytes:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())


def verify_password(pw: str, hashed) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    try:
        return bcrypt.checkpw(pw.encode("utf-8"), hashed)
    except Exception:
        return False


def ensure_seed_users():
    if users.count_documents({}) > 0:
        return
    users.insert_many([
        {
            "email": "demo@cogniscan.ai",
            "name": "Demo User",
            "password_hash": hash_password("demo1234"),
            "role": "user",
            "created_at": now(),
        },
        {
            "email": "admin@cogniscan.ai",
            "name": "Admin",
            "password_hash": hash_password("admin1234"),
            "role": "admin",
            "created_at": now(),
        },
    ])


def find_user(email: str, role: str):
    return users.find_one({"email": email.strip().lower(), "role": role})


def login(email: str, password: str, role: str):
    user = find_user(email, role)
    if not user:
        return None
    if not verify_password(password, user.get("password_hash")):
        return None
    return user


def register(email: str, name: str, password: str, role: str = "user"):
    email = email.strip().lower()
    if users.find_one({"email": email, "role": role}):
        return None
    doc = {
        "email": email,
        "name": name,
        "password_hash": hash_password(password),
        "role": role,
        "created_at": now(),
    }
    res = users.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc
