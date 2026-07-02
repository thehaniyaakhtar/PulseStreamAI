import redis
from aggregator import update_summary, trend_summary

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses=True
)

STREAM_NAME = "social_posts"

def consume_posts():

    last_id = "0"

    while True:

        messages = redis_client.xread(
            {STREAM_NAME: last_id},
            block=5000
        )

        if not messages:
            continue

        for stream_name, events in messages:

            for stream_id, post in events:

                update_summary(post)

                print("\nCurrent Trend Summary")
                print("-" * 30)

                for hashtag, stats in trend_summary.items():
                    print(
                        f"{hashtag} | "
                        f"Posts: {stats['posts']} | "
                        f"Likes: {stats['likes']} | "
                        f"Comments: {stats['comments']} | "
                        f"Shares: {stats['shares']}"
                    )

                print("-" * 30)

                last_id = stream_id
    
    
if __name__=="__main__":
    consume_posts()