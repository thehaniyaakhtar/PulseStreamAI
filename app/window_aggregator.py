import time
from collections import defaultdict
# defaultdict enables creation of a new dict when new #/key is seen
from datetime import datetime
# stores timestamps
import pandas as pd

WINDOW_SIZE = 10 # seconds 
# each stat lasts for 60 seconds

# Store stats for CURRENT time window
# defaultdict automatically creates a new dict wnv a new # is encountered
current_window = defaultdict(
    lambda: {
        "posts": 0,
        "likes": 0,
        "comments": 0,
        "shares": 0,
        "impressions": 0,
        "watch_time": 0,
        "ctr": 0,
        "sentiment": 0,
        "engagement_velocity": 0
    }
)

# Stores the completed windows which is later replaced with CSV
window_history = []

window_start = time.time()

def update_window(post):
    # update the stats for current window using newly received post
    
    hashtag = post["hashtag"]
    
    # Increase the number of posts for given hashtag
    current_window[hashtag]["posts"] += 1
    
    # Redis returns string so convert to integer
    current_window[hashtag]["likes"] += int(post["likes"])
    current_window[hashtag]["comments"] += int(post["comments"])
    current_window[hashtag]["shares"] += int(post["shares"])
    
    current_window[hashtag]["impressions"] += int(post["impressions"])

    current_window[hashtag]["watch_time"] += float(post["watch_time"])

    current_window[hashtag]["ctr"] += float(post["ctr"])

    current_window[hashtag]["sentiment"] += float(post["sentiment"])

    current_window[hashtag]["engagement_velocity"] += float(
        post["engagement_velocity"]
)
    
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
            "shares": stats["shares"],
            "impressions": stats["impressions"],
            "watch_time": stats["watch_time"],
            "ctr": stats["ctr"],
            "sentiment": stats["sentiment"],
            "engagement_velocity": stats["engagement_velocity"]
        }
        
        # save it into historical dataset
        window_history.append(row)
        
    # Start fresh from new window
    current_window.clear()
        

# process incoming osts
def process_post(post):
    # called once for every post received by the consumer
    
    global window_start
    # you want the one defined at top of the file
    
    update_window(post)
    # update counters of # when a new post arrives
    
    current_time = time.time()
    # gets current time
    if current_time - window_start >= WINDOW_SIZE:
        # Has one minute passed?
        print("\nWindow finalized\n")
        finalize_window()
        window_start = current_time # Start a new timer

def export_dataframe():
    # Convert all completed windows into a pandas df
    df = pd.DataFrame(window_history)
    return df

def export_csv(filename = "trend_dataset.csv"):
    # saves the completed windows as CSV
    df = export_dataframe()
    df.to_csv(filename, index = False) 
    print(f"Dataset exported to {filename}")