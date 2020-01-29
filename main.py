import os
import logging
import requests
import praw


def notify_channel(submission):
    payload = {
        'embeds': [
            {
                'title': submission.title,
                'type': 'rich',
                'url': '%s%s' % ('https://reddit.com', submission.permalink),
                'fields': [
                    {
                        'name': 'Subreddit',
                        'value': submission.subreddit.display_name,
                        'inline': True
                    },
                    {
                        'name': 'Author',
                        'value': submission.author.name,
                        'inline': True
                    }
                ]
            }
        ]
    }
    url = os.getenv('DISCORD_WEBHOOK')
    resp = requests.post(url, json=payload)
    resp.raise_for_status()


def main():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
    handler.setFormatter(formatter)

    logger = logging.getLogger('RedditWatcher')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    while True:
        try:
            logger.info('Starting RedditWatcher')
            reddit = praw.Reddit(client_id=os.getenv('PRAW_CLIENT_ID'), client_secret=os.getenv(
                'PRAW_CLIENT_SECRET'), user_agent='RedditWatcher/1.0')
            for submission in reddit.subreddit('all').stream.submissions():
                if 'malwarebytes' in submission.selftext.lower() or 'malwarebytes' in submission.title.lower():
                    notify_channel(submission)
        except Exception as ex:
            logger.error(ex)
            continue


if __name__ == '__main__':
    main()
