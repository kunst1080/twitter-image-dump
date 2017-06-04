import os
import sys
import twitter

def get_twitter():
    config_file = os.getenv("HOME") + os.sep + "twitter.key"
    conf = None
    if os.path.isfile(config_file):
        try:
            with open(config_file, 'r') as file:
                conf = config_to_dictionary(file)
        except IOError:
            die(config_file + ":file cannot open.")
    else:
        die(config_file + ":file not exists.")
    auth = twitter.OAuth(consumer_key=conf["CONSUMER_KEY"],
                         consumer_secret=conf["CONSUMER_SECRET"],
                         token=conf["ACCESS_TOKEN"],
                         token_secret=conf["ACCESS_TOKEN_SECRET"])
    return twitter.Twitter(auth=auth)

def config_to_dictionary(file):
    dic = {}
    for line in file:
        key, val = line.strip().split("=")
        dic[key] = val
    return dic

def die(message):
    print("ERROR:" + message, file=sys.stderr)
    sys.exit(1)
