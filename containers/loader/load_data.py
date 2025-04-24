import pickle
import numpy as np
import pandas as pd
import pymongo
import os

import pymongo.collection
from dotenv import load_dotenv

COLOUMNS = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
            "wrong_fragment","urgent","hot","num_failed_logins","logged_in",
            "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
            "num_shells","num_access_files","num_outbound_cmds","is_host_login",
            "is_guest_login","count","srv_count","serror_rate", "srv_serror_rate",
            "rerror_rate","srv_rerror_rate","same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
            "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
            "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
            "dst_host_rerror_rate","dst_host_srv_rerror_rate","attack", "last_flag"]

class NetworkLoader(object):
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.database: pymongo.collection.ClientSession = self._get_database("NETWORK")

    
    def load_data(self, dataframe, collection_name):
        collection = self.database[collection_name]
        records = dataframe.to_dict('records')
        collection.insert_many(records)

    def run(self):
        print("Loading Data...")
        train_df = pd.read_csv("./data/Train.txt", names=COLOUMNS)
        self.load_data(train_df, "train")
        test_df = pd.read_csv("./data/Test.txt", names=COLOUMNS)
        self.load_data(test_df, "test")
        print(f"Database has {self.collection.count_documents({})} entires")

    def _get_database(self, database):
        try:
            database_url = os.environ.get("DATABASE_URL")
            client = pymongo.MongoClient(database_url)
            client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(err)
            print("Are you sure your database is on and this can reach it?")
        return client[database]

    def _clean_db_check(self) -> bool:
        try:
            return True if int(os.getenv('SCRUB_DB')) == 1 else False
        except:
            return False
         
    def _scrub_db(self, db, collection):
        db[collection].drop()

if __name__ == "__main__":
    print("Starting...")
    dirpath = "./cifar-100-python/"
    dataloader = CifarLoader(dirpath)
    dataloader.run()
    print("Ending...")