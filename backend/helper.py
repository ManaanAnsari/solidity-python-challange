import json
import os
import pandas as pd
from config import Config

'''
this file contains helper functions that are used in the main server file
'''


class Helper:
    def __init__(self) -> None:
        self.conf = Config()
    
    def storeCache(self,data:dict):
        # this stores the cache data to a file
        with open(self.conf.CACHE_FILE, 'w') as f:
            json.dump(data, f)
        return data

    def getCachedData(self):
        # this loads the cache data from a file
        if os.path.isfile(self.conf.CACHE_FILE):
            with open(self.conf.CACHE_FILE, 'r') as f:
                data = json.load(f)
                return data
        else:
            return self.storeCache({})
            
            
    def dumpDF(self,df):
        # this function stores the main events dataframe to a file
        df.to_csv(self.conf.EVENTS_FILE, index=False)
        return df

    def loadDF(self):
        # this function loads the main events dataframe from a file if exists
        if os.path.isfile(self.conf.EVENTS_FILE):
            df = pd.read_csv(self.conf.EVENTS_FILE)
            return df
        else:
            # if the file does not exist, return an empty dataframe
            return pd.DataFrame(columns=["blockNumber", "event", "user", "amount", "locked_balance", "is_reward_distributed"])

    def getOrStorePreviousBlock(self,cache,previous_block = None):
        # this function gets or stores the previous block number
        # mainly because we want to keep track of the last block number we processed
        # so that even if the server restarts, we can continue from the last block number
        if previous_block is not None:
            cache["previous_block"] = previous_block
            self.storeCache(cache)
            return previous_block
        else:
            return cache.get("previous_block", None)
            
    def cleanDf(self,df, from_block):
        #  this function cleans the main events dataframe
        # to avoid processing the same events again (duplicates)
        df = df[df['blockNumber'] < from_block]
        return df