import time
import pandas as pd
from web3_helper import Web3Helper

'''
this is the main server file that will be running in the background
it will be listening to the events on the blockchain
and will be distributing the rewards to the users
'''

w3_helper = Web3Helper()
helper = w3_helper.helper
conf = helper.conf
global_cache = helper.getCachedData()
X = conf.X
decimals = 18

# check if we have processed any blocks before
previous_block_processed = helper.getOrStorePreviousBlock(global_cache)
# if not, then get the current block number
if previous_block_processed is None:
    previous_block_processed =w3_helper.web3.eth.block_number 
    helper.getOrStorePreviousBlock(global_cache,previous_block_processed)
# calculate the next trigger block
next_trigger_block = previous_block_processed + X

# this is the event filter for the deposit and withdraw events
# note : we start listening from the last block we processed
deposit_filter = w3_helper.airvault_contract.events.Deposit.create_filter(fromBlock=previous_block_processed)
withdraw_filter = w3_helper.airvault_contract.events.Withdraw.create_filter(fromBlock=previous_block_processed)

# this is the main events dataframe
# we load it from the file if it exists
events_df = helper.loadDF()
# we clean the dataframe to avoid processing the same events again
events_df = helper.cleanDf(events_df, previous_block_processed)


def eventHandler(event):
    print(event["args"])
    print(event["event"], event["blockNumber"])
    # log the event
    # this will store the event in the main events dataframe
    # so that we can distribute rewards later
    if event["event"] in ["Deposit", "Withdraw"]:
        row = {}
        row["blockNumber"] = event["blockNumber"]
        row["event"] = event["event"]
        row["user"] = event["args"]["user"]
        row["amount"] = event["args"]["amount"]
        row["locked_balance"] = event["args"]["locked_balance"]
        row["is_reward_distributed"] = False
        global events_df
        events_df = pd.concat([events_df, pd.DataFrame([row])], ignore_index=True)
        helper.dumpDF(events_df)



def airdropRewards(current_block, reward_block_start):
    global events_df
    print("Distributing rewards")

    # Filter the relevant events from the last x blocks
    relevant_events = events_df[(events_df['blockNumber'] > reward_block_start) & (events_df['blockNumber'] <= current_block) & (events_df['is_reward_distributed'] == False)]

    # if there are no events to distribute rewards for, then return
    if relevant_events.empty:
        print("No events to distribute rewards for.")
        return

    # Calculate rewards for each user
    users = relevant_events['user'].unique()
    for user in users:
        user_events = relevant_events[relevant_events['user'] == user]
        # do the main reward calculation 
        
        # WIN tokens in airdrop = 0.05 * (# FUD tokens deposited) * (# blocks deposited) / ( total # blocks)
        # Calculate the weighted FUD deposits
        weights = current_block - user_events['blockNumber']
        deposits = user_events['amount'] * weights
        deposits[user_events['event'] == 'Withdraw'] *= -1

        total_fud = deposits.sum()
        total_blocks = weights.sum()

        avg_fud = total_fud / total_blocks if total_blocks != 0 else 0
        win_tokens_amt = 0.05 * avg_fud
        win_tokens_amt = int(win_tokens_amt)
        win_tokens_amt = max(0, win_tokens_amt)
        # if no rewards to distribute, then skip
        if win_tokens_amt:
            win_tokens_amt = win_tokens_amt*10**decimals
            # do the main minting and distribution of WIN tokens
            # note: this can be done in an async way which will be much better and faster
            w3_helper.mint_win_tokens(user, win_tokens_amt)
            print(f"Distributed {win_tokens_amt} WIN tokens to {user}")
        # Mark these events as distributed
        events_df.loc[user_events.index, 'is_reward_distributed'] = True
    helper.dumpDF(events_df)

def main():
    global previous_block_processed, next_trigger_block, X, global_cache, events_df
    while True:
        # the main server loop
        
        # log all the deposit and withdraw events
        for event in deposit_filter.get_new_entries():
            eventHandler(event)
        for event in withdraw_filter.get_new_entries():
            eventHandler(event)
            
        # check if the block number is equal to the next trigger block
        b_no = w3_helper.web3.eth.block_number
        if b_no >= next_trigger_block:
            # air drop the rewards
            airdropRewards(next_trigger_block,previous_block_processed)
            # store the processed block number
            previous_block_processed = b_no
            next_trigger_block = b_no + X
            helper.getOrStorePreviousBlock(global_cache,previous_block_processed)
        time.sleep(10)

if __name__ == "__main__":
    main()