import os

import firebase_admin as fb
import google.cloud.firestore_v1
from firebase_admin import firestore as FIRESTORE


cred = fb.credentials.Certificate(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "creds.json")
)
fb.initialize_app(cred)

db: google.cloud.firestore_v1.client.Client = fb.firestore.client()

db.collection("Users").document("test").set({"test": "test"})
