"""AIOS-FORGE - Social Media Service (Twitter/X)"""
from config import get_key

def tweet(text, image_path=None, mention=None):
    """Post to Twitter/X (FREE - 500 posts/month)"""
    consumer_key = get_key("twitter_consumer_key")
    consumer_secret = get_key("twitter_consumer_secret")
    access_token = get_key("twitter_access_token")
    access_secret = get_key("twitter_access_secret")

    if not all([consumer_key, consumer_secret, access_token, access_secret]):
        print("  \033[31m✗\033[0m Twitter API keys nao configuradas")
        print("    1. Crie app em: https://developer.twitter.com/en/portal/projects-and-apps")
        print("    2. Configure:")
        print("       forge config twitter_consumer_key KEY")
        print("       forge config twitter_consumer_secret SECRET")
        print("       forge config twitter_access_token TOKEN")
        print("       forge config twitter_access_secret SECRET")
        return None

    try:
        import tweepy

        if mention:
            text = f"{text} @{mention}"

        if image_path:
            # V1 API for media upload
            auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_secret)
            api = tweepy.API(auth)
            media = api.media_upload(str(image_path))

            # V2 client for tweet
            client = tweepy.Client(
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_secret,
            )
            response = client.create_tweet(text=text, media_ids=[media.media_id])
        else:
            client = tweepy.Client(
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_secret,
            )
            response = client.create_tweet(text=text)

        tweet_id = response.data["id"]
        print(f"  \033[32m✓\033[0m Tweet postado!")
        print(f"    https://twitter.com/i/web/status/{tweet_id}")
        return tweet_id

    except ImportError:
        print("  \033[31m✗\033[0m tweepy nao instalado")
        print("    Instale: pip3 install tweepy")
        return None
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro Twitter: {e}")
        return None

def twitter_action(action, target=None):
    """Twitter actions: like, retweet, follow, delete"""
    consumer_key = get_key("twitter_consumer_key")
    consumer_secret = get_key("twitter_consumer_secret")
    access_token = get_key("twitter_access_token")
    access_secret = get_key("twitter_access_secret")

    if not all([consumer_key, consumer_secret, access_token, access_secret]):
        print("  \033[31m✗\033[0m Twitter API keys nao configuradas")
        return None

    try:
        import tweepy
        client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_secret,
        )

        if action == "like" and target:
            client.like(target)
            print(f"  \033[32m✓\033[0m Liked tweet {target}")
        elif action == "retweet" and target:
            client.retweet(target)
            print(f"  \033[32m✓\033[0m Retweeted {target}")
        elif action == "follow" and target:
            client.follow_user(target)
            print(f"  \033[32m✓\033[0m Following {target}")
        elif action == "delete" and target:
            client.delete_tweet(target)
            print(f"  \033[32m✓\033[0m Deleted tweet {target}")
        else:
            print(f"  \033[31m✗\033[0m Acao desconhecida: {action}")
            return None
        return True
    except Exception as e:
        print(f"  \033[31m✗\033[0m Erro: {e}")
        return None
