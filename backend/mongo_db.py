import os
import pymongo
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = os.environ.get("MONGO_URI")

class MongoDBStore:
    def __init__(self, uri=None):
        self.uri = uri or MONGO_URI
        self.client = None
        self.db = None
        self.connected = False
        self._init_connection()

    def _init_connection(self):
        try:
            self.client = pymongo.MongoClient(
                self.uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=4000
            )
            # Ping database
            self.client.admin.command('ping')
            self.db = self.client.get_database('multimodal_doc_intelligence')
            self.connected = True
            print("[MongoDB Store] Successfully connected to MongoDB Atlas!")
        except Exception as e:
            print(f"[MongoDB Store] MongoDB Atlas Connection Note: {e} (operating with local JSON index & MongoDB sync ready)")
            self.connected = False

    def save_document(self, doc_data):
        if self.connected and self.db is not None:
            try:
                self.db.documents.update_one(
                    {"doc_id": doc_data["doc_id"]},
                    {"$set": doc_data},
                    upsert=True
                )
            except Exception as e:
                print(f"[MongoDB Store] Save document error: {e}")

    def save_query_log(self, query_record):
        if self.connected and self.db is not None:
            try:
                self.db.query_logs.insert_one(query_record)
            except Exception as e:
                print(f"[MongoDB Store] Save query log error: {e}")

    def save_eval_benchmark(self, eval_data):
        if self.connected and self.db is not None:
            try:
                self.db.eval_benchmarks.insert_one(eval_data)
            except Exception as e:
                print(f"[MongoDB Store] Save benchmark error: {e}")

    def get_query_history(self, limit=10):
        if self.connected and self.db is not None:
            try:
                cursor = self.db.query_logs.find({}, {"_id": 0}).sort("_id", -1).limit(limit)
                return list(cursor)
            except Exception as e:
                print(f"[MongoDB Store] Get history error: {e}")
        return []
