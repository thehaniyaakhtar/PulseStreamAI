# imports
import redis
from faker import Faker
import random
from datetime import datetime
import time

# Create a Faker object to generate realistic fake data
fake = Faker()

# name of redis stream where posts will be stored
STREAM_NAME  = "social_posts"

# Hashtag Popularity
# Assigned numbers act as weights, not %
HASHTAG_POPULARITY = {
    "#AI": 35,
    "#Python": 25,
    "#DataScience": 15,
    "#MachineLearning": 10,
    "#Climate": 10,
    "#Football": 5
}

# Possible media attached to a post
MEDIA_TYPES = ["image", "video", "text"]

# User Profiles
# Each profile contains, follower count range
# expected engagement rate range
# if acc is verified

USER_TYPES = {
    "casual": {
        "followers": (100, 5_000),
        "engagement": (0.04, 0.10),  # 4% - 10%
        "verified": False
    },
    "creator": {
        "followers": (5_000, 100_000),
        "engagement": (0.02, 0.06),  # 2% - 6%
        "verified": False
    },
    "celebrity": {
        "followers": (100_000, 5_000_000),
        "engagement": (0.01, 0.03),  # 1% - 3%
        "verified": True
    }
}

# Connecting to the Redis server
# Redis Connection
# Connect to the local Redis server
# decode_response = True converts Redis bytes into Python strings

redis_client = redis.Redis(
    host = "localhost",         # Redis is running on the same machine
    port = 6379,                # Default Redis port
    decode_responses= True      # AUtomatically decode bytes into Python string
)

def generate_user():
    # Generate a random user profile
    user_type = random.choices(
        list(USER_TYPES.keys()),
        weights=[80, 18, 2],
        k = 1
    )[0]
    
    # Retrieve settings for selected user type
    profile = USER_TYPES[user_type]
    
    return{
        "user_id": fake.uuid4(),
        "user_type": user_type,
        "followers": random.randint(*profile["followers"]),
        "verified": profile["verified"],
        "country": fake.country()
    }

def generate_content():
    # Generate the content of a social media post
    
    # chooe a hashtag based on weighted probability
    # Poplar hashtags appear more frequently
    hashtag = random.choices(
        list(HASHTAG_POPULARITY.keys()),
        weights= HASHTAG_POPULARITY.values(),
        k = 1
    )[0]
    
    return {
        "hashtag": hashtag,
        "caption": fake.sentence(nb_words=10),
        "media_type": random.choice(MEDIA_TYPES)
    }
    
def generate_engagement(user, content):
    # Estimate likes, comments and shares based on popularity, engagement rate etc
    # get engagment range for users category
    profile = USER_TYPES[user["user_type"]]
    
    # pick a random engagement rate within allowed range
    engagement_rate  = random.uniform(
        profile["engagement"][0],
        profile["engagement"][1]
    )
    
    # Popular hashtags to slightly increase engagement
    hashtag_boost = 1 + (
        HASHTAG_POPULARITY[content["hashtag"]] / 100                 
    )
    
    media_boost = {
        "text": 1.0, 
        "image": 1.1,
        "video": 1.3
    }
    
    likes = int(
        user["followers"]
        * engagement_rate
        * hashtag_boost
        * media_boost[content["media_type"]]
    )
    
    comments = int(likes * random.uniform(0.05, 0.15))
    shares = int(likes * random.uniform(0.02, 0.10))
    
    return{
        "likes": likes,
        "comments": comments,
        "shares": shares
    }

def generate_post():
    # combine user data, content, engagement into single media post
    # generate each component
    user = generate_user()
    content = generate_content()
    engagement = generate_engagement(user, content)

    return {
        "post_id": fake.uuid4(),
        "timestamp": datetime.now().isoformat(),
        
        **user,
        **content,
        **engagement
    }

def stream_posts():
    # continuously generate posts and push them into Redis stream
    # A new post is generated every second
    while True:
        post = generate_post()
        
        # Add post to Redis stream
        # xadd() retrned the ID assigned by Redis
        stream_id = redis_client.xadd(
            STREAM_NAME,
            post
        )
        
        # Print the stream ID and hashtag for monitoring
        print(f"Sent: {stream_id} | {post['hashtag']}")
        
        # Wait for 1 secons before generating the next post
        time.sleep(1)

if __name__ == "__main__":
    stream_posts()