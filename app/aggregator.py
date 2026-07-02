trend_summary = {}

def update_summary(post):
    hashtag = post["hashtag"]
    
    if hashtag not in trend_summary:
        trend_summary[hashtag] = {
            "posts": 0,
            "likes": 0,
            "comments": 0,
            "shares": 0
        }

    trend_summary[hashtag]["posts"] += 1
    trend_summary[hashtag]["likes"] += int(post["likes"])
    trend_summary[hashtag]["comments"] += int(post["comments"])
    trend_summary[hashtag]["shares"] += int(post["shares"])
