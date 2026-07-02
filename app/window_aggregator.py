import time
from collections import defaultdict
# defaultdict enables creation of a new dict when new # is seen
from datetime import datetime
import pandas as pd

WINDOW_SIZE = 60

# Store stats for CURRENT time window
# defaultdict automatically creates a new dict wnv a new # is encountered
current_window = defaultdict(
    lambda: {
        "posts": 0,
        "likes": 0,
        "comments": 0,
        "shares": 0
    }
)

# Stores the finalized windows which is later replaced with CSV
window_history = []

def update_window(post):
    # update the stats for current window using newly received post
    
    hashtag = post["hashtag"]
    
    # Increase the number of posts for given hashtag
    current_window[hashtag]["posts"] += 1
    
    # Redis returns string so convert to integer
    current_window[hashtag]["likes"] += int(post["likes"])
    current_window[hashtag]["comments"] += int(post["comments"])
    current_window[hashtag]["shares"] += int(post("shares"))
    
def finalize_window():
    # Creates one snapshot of the current time window
    # saves it and resets the counter to the next window
    
    # Capture the current time.
    # Serves as timestamp for every row created during this window
    timestamp = datetime.now().replace(second = 0, microsecond=0)
    
    # Go through every # seen in the window
    for hashtag, stats in current_window.items():
        row = {
            "timestamp": timestamp,
            "hashtag": hashtag,
            "posts": stats["posts"],
            "likes": stats["likes"],
            "comments": stats["comments"],
            "shares": stats["shares"]
        }
        
        # save it into historical dataset
        window_history.append(row)
        
    # Start fresh from new window
    current_window.clear()
        

# process incoming posts
def process_post(post):
    
    # called once for every post received by the consumer
    global window_start
    # you want the one defined at  top of the file
    update_window(post)
    # update counters when a new post arrives
    current_time = time.time()
    if current_time - window_start >= WINDOW_SIZE:
        print("\nWindow finalized\n")
        finalize_window()
        window_start = current_time

def export_dataframe():
    # Convert all completed windows into a pandas df
    df = pd.DataFrame(window_history)
    return df

def export_csv(filename = "trend_dataset.csv"):
    # saves the completed windows as CSV
    df = export_dataframe()
    df.to_csv(filename, index = False) 
    print(f"Dataset exported to {filename}")