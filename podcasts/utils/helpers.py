def get_twitter_tag(twitter_url):
    if twitter_url:
        twitter_tag = twitter_url.split("/")[-1]
        return f"@{twitter_tag}"
    else:
        return None
