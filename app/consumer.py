import redis

# import function that updates hashtag stats + dictionary that stores aggregated results
from aggregator import update_summary, trend_summary

# Redis connection
redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses=True
)

STREAM_NAME = "social_posts"

# consume posts from redis stream
def consume_posts():
    # continuously reads posts from Redis Stream
    # update the hashtag summary
    # print current stats
    last_id = "0"
    
    # keep listening to new posts forever
    while True:
        # Read new message from the stream
        # {STREAM_NAME: last_id}: Read all messages with ID greater than last_id
        # block=5000: Wait for 5000 ms for new msgs
        messages = redis_client.xread(
            {STREAM_NAME: last_id},
            block = 5000
        )
        
        # If no new meesages arrive within 5 seconds, continue waiting
        if not messages: continue
        
        # messages is a list containing one or more streams
        # each item contains
        for stream_name, events in messages:
            # events is a list of:
            # (stream_id, post_dictionary)
            for stream_id, post in events:
                # Update hashatg stats using this post
                update_summary(post)
                
                # print the latest aggregateed stats
                print("\nCurrent Trend Summary")
                print("-" * 30)
                
                # Loop through every hashtag collected so far
                for hashtag, stats in trend_summary.items():
                    print(
                        f"{hashtag} | "
                        f"Posts: {stats['posts']} | "
                        f"Likes: {stats['likes']} | "
                        f"Comments: {stats['comments']} | "
                        f"Shares: {stats['shares']}"
                    )
                print("-" * 30)
                
                # Save current stream ID
                last_id = stream_id # xread() will only fetch newer messages

if __name__ == "__main__":
    consume_posts()