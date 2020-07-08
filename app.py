import tweepy
import os
import requests
import time


def makeTweet():
    # set the url and the message
    query = requests.get("https://api.nasa.gov/planetary/apod",
                         params={"api_key": os.getenv("NASA"),
                                 "hd": True}).json()
    # From this json I must get the 'hdurl', media_type, 'title'
    media_type = query['media_type']
    if media_type == 'image':
        title = query['title']
        url = query['hdurl']
        message = f"{title}: copyright: {query['copyright']} {query['explanation']}"
        message = message[:276]
        message += '...'
        print(message)
        return url, message
    else:
        print("fail")
        return None


def main():
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)
    print('authenticated (not actually tbh)')
    
    INTERVAL = 60*60*24
    filename = 'temp.jpg'
    while True:
        apod = makeTweet()
        if apod is not None:
            url = apod[0]
            message = apod[1]

            # Rest of function is copy and pasted from StackOverflow user Brobin
            # https://stackoverflow.com/questions/31748444/how-to-update-twitter-status-with-image-using-image-url-in-tweepy
            request = requests.get(url, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)

                api.update_with_media(filename, status=message)
                os.remove(filename)
            else:
                print("Unable to download image")

        else:
            print('not an image')
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()


