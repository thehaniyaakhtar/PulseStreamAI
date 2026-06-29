import redis
from faker import Faker 
import random
from datetime import datetime
import time

fake = Faker()

STREAM_NAME = "social_posts"
def stream_posts():
    while True:
        post = generate_post()
        stream_id = redis_client.xadd(
            STREAM_NAME,
            post
        )
        print(f"Sent: {stream_id} | {post['hashtag']}")
        
        time.sleep(1)


# making a connection to Redis
# redis_client = redis.Redis(
#     host = "localhost",         # connecting to a service running on the same computer
#     port=6379,                  # where we chose to run Redis
#     decode_responses = True     # converts bytes into Python strings
# )

# dictionary of hashtags
# values are weights/ prob of choosing each hashtag 
HASHTAG_POPULARITY = {
    "#AI": 35,
    "#Python": 25,
    "#DataScience": 15,
    "#MachineLearning": 10,
    "#Climate": 10,
    "#Football": 5
}

MEDIA_TYPES = ["image", "video", "text"]

USER_TYPES = {
    "casual": {
        "followers": (100, 5_000),
        "engagement": (0.04, 0.10),
        "verified": False
    },
    "creator": {
        "followers": (5_000, 100_000),
        "engagement": (0.02, 0.06),
        "verified": False
    },
    "celebrity":{
        "followers": (100_000, 5_000_000),
        "engagement": (0.01, 0.03),
        "verified": True
    }
}

def generate_user():
    user_type = random.choices(
        list(USER_TYPES.keys()),
        weights=[80, 18, 2],
        k=1
    )[0]
    
    profile = USER_TYPES[user_type]
    
    return{
        "user_id": fake.uuid4(),
        "user_type": user_type,
        "followers": random.randint(*profile["followers"]),
        "verified": profile["verified"],
        "country": fake.country()
    }

# generating a function that returns realistic posts
def generate_content():
   
    # picking on hashtag
    hashtag = random.choices(
        list(HASHTAG_POPULARITY.keys()),
        weights=HASHTAG_POPULARITY.values(),
        k = 1
    )[0] # returns a list but you only want the string within
    
    return {
        "hashtag": hashtag,
        "caption": fake.sentence(nb_words=10), # faker generates random sentence
        "media_type": random.choice(MEDIA_TYPES) # icking one w equal probability
    }

    
def generate_engagement(user, content):
    profile = USER_TYPES[user["user_type"]]
    
    engagement_rate = random.uniform(
        profile["engagement"][0],
        profile["engagement"][1]
    )
    
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
    
    return {
        "likes": likes,
        "comments": comments,
        "shares": shares
    }

def generate_post():
    user = generate_user()
    content = generate_content()
    engagement = generate_engagement(user, content)
    
    return{
        "post_id": fake.uuid4(),
        "timestamp": datetime.now().isoformat(),
        
        **user,
        **content,
        **engagement
    }

# post = generate_post()
# print(post)

if __name__ == "__main__":
    stream_posts()