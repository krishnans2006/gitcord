import os

import firebase_admin as fb
import google.cloud.firestore_v1
from firebase_admin import firestore as FIRESTORE


cred = fb.credentials.Certificate(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "creds.json")
)
fb.initialize_app(cred)

db: google.cloud.firestore_v1.client.Client = fb.firestore.client()


def get_user_defaults(user_id: int, tag: str):
    doc = db.collection("Users").document(str(user_id))

    doc.set({"Tag": tag}, merge=True)

    return doc.get().to_dict().get("Defaults")


def set_user_defaults(user_id: int, tag: str, defaults: dict):
    doc = db.collection("Users").document(str(user_id))

    doc.set({"Tag": tag, "Defaults": defaults}, merge=True)

    return True
