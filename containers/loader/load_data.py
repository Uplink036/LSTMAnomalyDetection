import logging
import os
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from logger import configure_loggers

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
    def __init__(self):
        self.database = self._get_database("NETWORK")
    
    def load_data(self, dataframe, collection_name):
        collection = self.database[collection_name]
        records = dataframe.to_dict('records')
        collection.insert_many(records)
        print(f"Collection - {collection_name} now has {collection.count_documents({})} entires")
        logger.info(f"Collection - {collection_name} has {collection.count_documents({})} entires")

    def run(self):
        print("Checking database")
        logger.info("Checking database")        
        if self._clean_db_check():
            self._scrub_db("train")
            self._scrub_db("test")

        print("Loading Data...")
        logger.info("Loading Data...")
        train_df = pd.read_csv("./data/Train.txt", names=COLOUMNS)
        self.load_data(train_df, "train")
        test_df = pd.read_csv("./data/Test.txt", names=COLOUMNS)
        self.load_data(test_df, "test")

    def _get_database(self, database):
        try:
            database_url = os.environ.get("DATABASE_URL")
            client = MongoClient(database_url)
            client.server_info()
        except ServerSelectionTimeoutError as err:
            print(err)
            logger.error(err)
            print("Are you sure your database is on and this can reach it?")
            logger.error("Are you sure your database is on and this can reach it?")            
        return client[database]

    def _clean_db_check(self) -> bool:
        try:
            return True if int(os.getenv('SCRUB_DB')) == 1 else False
        except:
            return False
         
    def _scrub_db(self, collection):
        self.database[collection].drop()

if __name__ == "__main__":
    configure_loggers("loader")
    logger = logging.getLogger("load_data.py")
    logger.setLevel(level=logging.INFO)
    print("Starting...")
    logger.info("Starting...")
    dataloader = NetworkLoader()
    dataloader.run()
    print("Ending...")
    logger.info("Ending...")