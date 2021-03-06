# crawler.py
#
# Simple Twitter Crawler that does stuff
# Created for CSRC Lab, PEC Univ
# Uses tweepy API wrapper
#
# Jaskirat Singh
# jaskiratsingh76@gmail.com
# March 2015
# Repo at: github.com/akhrot
#
# Note: Replace seed user at end of this file
#


# -*- coding: utf-8 -*-

import time
import datetime
import json
import string
import requests
import random
import os
import sys
import argparse
import tweepy
import math


class TwitterAPI(object):
    def __init__(self, api_index_list):
        self.theta = 1
        self.depth = 1
        self.userInfoFilename = "userinfo.json"
        self.tweetListFilename = "tweetList.json"
        self.processedTweetsFilename = "processedTweets.json"
        self.users_to_crawl = []
        self.crawled_users = {}
        self.api_index_to_use = api_index_list
        self.apis = self.get_apis()
        self.test_apis()
        self.blacklist = self.load_blacklisted_urls()
        self.dir_path = ""

    def set_depth(self, depth):
        self.depth = depth

    def set_tweet_filename(self, tweetfile):
        self.tweetListFilename = tweetfile

    def set_processed_tweets_filename(self, resultfile):
        self.processedTweetsFilename = resultfile

    def set_user_info_filename(self, userinfofile):
        self.userInfoFilename = userinfofile

    def set_probability_filename(self, messageFilename):
        self.messageFilename = messageFilename

    def test_apis(self):
        tested_apis = []
        print '-' * 15
        print "Testing API connections...",

        for api in self.apis:
            working = True
            try:
                me = api.me()
                print "PASS",
            except:
                print "FAIL",
                working = False

            if working:
                tested_apis.append(api)

        self.apis = tested_apis
        print
        print len(self.apis), "API connections valid"
        print '-' * 15

    def load_keys(self, file_name):
        path = "./keys/"
        file_content = open(path + file_name).read()
        return file_content.split("\n")

    def get_apis(self):
        consumer_keys_file = "consumer_keys.txt"
        consumer_secrets_file = "consumer_secrets.txt"
        access_tokens_file = "access_tokens.txt"
        access_secrets_file = "access_secrets.txt"

        consumer_keys = self.load_keys(consumer_keys_file)
        consumer_secrets = self.load_keys(consumer_secrets_file)
        access_tokens = self.load_keys(access_tokens_file)
        access_secrets = self.load_keys(access_secrets_file)

        api_list = []
        num_keys = len(consumer_keys)

        print "Using API index",
        for index in self.api_index_to_use:
            print index,
            # authenticate using tweepy
            api = ""
            auth = tweepy.OAuthHandler(consumer_keys[index], consumer_secrets[index])
            auth.set_access_token(access_tokens[index], access_secrets[index])
            api = tweepy.API(auth)
            api_list.append(api)

        print
        print '-' * 15,
        print len(api_list), "API connections established",
        print '-' * 15
        return api_list

    def load_blacklisted_urls(self):
        print "Loading blacklisted URLs..."

        file_name = "blacklisted_urls.txt"
        urls = open(file_name).read().split("\n")
        blacklist = {}
        for url in urls:
            url = url.strip()
            if blacklist.get(url, -1) == -1:
                blacklist[url] = 1
        print len(blacklist), "URLs loaded"
        print "-" * 20
        return blacklist

    def begin_sleep_sequence(self):
        print
        print "~" * 20,
        print "Sleeping",
        print "~" * 20
        time.sleep(30)
        print "*" * 20,
        print "Waking Up",
        print "*" * 20

    def get_user(self, user):
        try:
            api = random.choice(self.apis)
            return api.get_user(user)
        except tweepy.error.TweepError as err:
            try:
                if err[0][0]['code'] == 88:
                    self.begin_sleep_sequence()
                    return self.get_user(user)
            except TypeError as e:
                return -1

    def get_intersection_users(self, followers, following):
        # returns a list of users ids in intersection
        # of followers and following
        intersection = []
        user_map = {}

        for user in followers:
            if user_map.get(user, 0) == 0:
                user_map[user] = 1

        # calculate any duplicate users
        for user in following:
            if user_map.get(user, 0) == 1:
                intersection.append(user)

        return intersection

    def get_followers_list(self, user_id):
        # returns list of INTs (twitter ids)
        try:
            api = random.choice(self.apis)
            return api.followers_ids(user_id)
        except tweepy.error.TweepError as err:
            try:
                if err[0][0]['code'] == 88:
                    self.begin_sleep_sequence()
                    return self.get_followers_list(user_id)
            except TypeError as e:
                return []


    def get_following_list(self, user_id):
        # returns list of INTs (twitter ids)
        try:
            api = random.choice(self.apis)
            return api.friends_ids(user_id)
        except tweepy.error.TweepError as err:
            try:
                if err[0][0]['code'] == 88:
                    self.begin_sleep_sequence()
                    return self.get_following_list(user_id)
            except TypeError as e:
                return []

    def add_following(self, following_list):
        # followers: list of user ids
        for user in following_list:
            if self.crawled_users.get(user, -1) == -1:
                self.users_to_crawl.append(user)

    def get_tweets(self, user_id):
        try:
            api = random.choice(self.apis)
            return api.user_timeline(user_id, count = 100)
        except tweepy.error.TweepError as err:
            try:
                if err[0][0]['code'] == 88:
                    self.begin_sleep_sequence()
                    return self.get_tweets(user_id)
            except TypeError as e:
                return []

    def extract_user_details(self, user):
        # extract required details from user object
        # and write to FILE 1
        data_user_info = {}
        data_user_info['userid'] = str(user.id)
        data_user_info['screen_name'] = (user.screen_name.encode('utf-8'))
        data_user_info['description'] = user.description.encode('utf-8')
        data_user_info['name'] = user.name.encode('utf-8')
        data_user_info['location'] = user.location.encode('utf-8')
        data_user_info['statuses_count'] = str(user.statuses_count)
        data_user_info['followers_count'] = str(user.followers_count)
        data_user_info['friends_count'] = str(user.friends_count)
        data_user_info['created_at'] = str(user.created_at.date())
        data_user_info['profile_image_url'] = str(user.profile_image_url).replace("normal", "400x400")

        # calculate age of account (in days)
        old = user.created_at.date()
        today = datetime.date.today()
        age_in_days = (today - old).days
        data_user_info['age_in_days'] = str(age_in_days)

        # write json row to file
        file_path = self.dir_path + self.userInfoFilename
        with open(file_path, 'a') as fp:
            json.dump(data_user_info, fp)
            fp.write(os.linesep)

    def get_full_url(self, short_url):
        try:
            full_url = requests.head(short_url).headers['location']
            slashes = False
            if 'http://www' not in full_url or 'https://www' not in full_url:
                domain_start = full_url.find('//')
                slashes = True
            else:
                domain_start = full_url.find('.')

            if slashes:
                domain_end = full_url.find('/', domain_start + 2)
            else:
                domain_end = full_url.find('/', domain_start)

            if domain_end == -1:
                domain_end = full_url.find(" ", domain_start)

            if domain_end == -1:
                if slashes:
                    return full_url[domain_start + 2:]
                else:
                    return full_url[domain_start + 1:]
            else:
                if slashes:
                    return full_url[domain_start + 2: domain_end]
                else:
                    return full_url[domain_start + 1: domain_end]
        except:
            return ""

    def check_if_reply(self, tweet):
        # returns 1 if tweet contains `@`, else 0
        for char in tweet:
            if char == '@':
                return 1
        return 0

    def count_hashtags(self, tweet):
        # returns number of `#` in tweet
        count = 0
        for char in tweet:
            if char == '#':
                count += 1
        return count

    def check_url(self, tweet):
        # returns 1 if tweet contains url, else 0
        test_1 = "http://t.co/"
        test_2 = "https://t.co/"

        if test_2 in tweet or test_1 in tweet:
            return 1
        return 0

    def get_user_id(self, twitter_handle):
        try:
            api = random.choice(self.apis)
            user = api.get_user(twitter_handle)
            return user.id
        except tweepy.error.TweepError as err:
            try:
                if err[0][0]['code'] == 88:
                    self.begin_sleep_sequence()
                    return self.get_user_id(twitter_handle)
            except TypeError as e:
                return -1
        except:
            return -1

    def check_intersecting_user_reply(self, tweet, intersection):
        # returns 1 if the user being replied to
        # belongs to the intersecting user list, 0 otherwise
        handle = ""
        reply_start = tweet.find('@')
        if reply_start == -1:
            return 0

        test_string = tweet[reply_start + 1:]
        test_string = test_string.lower()
        for char in test_string:
            if char in string.lowercase or char in string.digits or char == '_':
                # part of twitter handle
                handle += char
            else:
                break

        # get user id (INT) of the twitter handle
        user_id = self.get_user_id(handle)

        # check if twitter handle belongs to intersection
        return int(user_id in intersection)

    def check_spam_url(self, tweet):
        # returns 1 if url is blacklisted, else 0
        # extract url from tweet
        test_1 = "http://t.co/"
        test_2 = "https://t.co/"

        if test_1 in tweet:
            test_string = test_1
        elif test_2 in tweet:
            test_string = test_2
        else:
            return 0

        start_index = tweet.find(test_string)
        short_url = tweet[start_index: start_index + len(test_string) + 10]


        # get domain name
        domain = self.get_full_url(short_url)
        if domain == "":
            return 0
        elif 'www.' in domain:
            domain = domain.strip('www.')

        # match with blacklisted urls
        return self.blacklist.get(domain, 0)

    def extract_hashtags(self, tweet):
        hashtag_list = []

        test_string = tweet.lower()
        tag = ""

        while True:
            start_index = test_string.find('#')
            if start_index == -1:
                break

            test_string = test_string[start_index + 1:]

            counter = 0
            for char in test_string:
                counter += 1
                if char in string.lowercase or char in string.digits or char == '_':
                    tag += char
                else:
                    break

            # add the extracted hashtag to list
            hashtag_list.append(tag)
            tag = ""
            test_string = test_string[counter - 1:]

        return hashtag_list

    def extract_tweets(self, tweets, intersection):
        # tweets: list of tweets, made up of Tweet objects
        # write to FILE 2

        # open output FILE 2
        file_path_2 = self.dir_path + self.tweetListFilename

        # open output FILE 3
        file_path_3 = self.dir_path + self.processedTweetsFilename
        reply_count = 0
        hashtag_count = 0
        repeated_hashtag_count = 0
        url_tweet_count = 0
        spam_url_tweet_count = 0
        reply_to_intersection = 0
        hashtags_used = {}

        tweet_count = 0
        tweets_processed = False
        # read tweets
        for tweet in tweets:
            tweet_count += 1
            print tweet_count,
            tweets_processed = True
            data_tweet_info = {}
            data_tweet_info['tweet_author_id'] = str(tweet.author.id)
            data_tweet_info['tweet_text'] = tweet.text.encode('utf-8')
            data_tweet_info['tweet_created_at'] = str(tweet.created_at)
            data_tweet_info['tweet_source'] = tweet.source.encode('utf-8')
            # write data for FILE 2
            with open(file_path_2, 'a') as fp:
                json.dump(data_tweet_info, fp)
                fp.write(os.linesep)

            # extract data for FILE 3
            tweet_text = tweet.text.encode('utf-8')
            twitter_id = tweet.author.id

            is_reply = self.check_if_reply(tweet_text)

            if is_reply:
                reply_count += 1
                if len(intersection):
                    reply_to_intersection += self.check_intersecting_user_reply(tweet_text, intersection)

            has_hashtag = self.count_hashtags(tweet_text)
            if has_hashtag:
                hashtag_count += has_hashtag

                for hashtag in self.extract_hashtags(tweet_text):
                    if hashtags_used.get(hashtag, -1) == -1:
                        hashtags_used[hashtag] = 1
                    else:
                        hashtags_used[hashtag] += 1

            url_in_tweet = self.check_url(tweet_text)
            if url_in_tweet > 0:
                url_tweet_count += 1
                spam_url_tweet_count += self.check_spam_url(tweet_text)

        for value in hashtags_used.values():
            if value > 1:
                repeated_hashtag_count += 1

        # structure data for FILE 3
        if tweets_processed:

            data_processed_tweets = {}
            data_processed_tweets['twitter_id'] = str(twitter_id)
            data_processed_tweets['reply_count'] = str(reply_count)
            data_processed_tweets['intersection'] = str(len(intersection))
            data_processed_tweets['reply_to_intersection'] = str(reply_to_intersection)
            data_processed_tweets['hashtag_count'] = str(hashtag_count)
            data_processed_tweets['repeated_hashtag_count'] = str(repeated_hashtag_count)
            data_processed_tweets['url_tweet_count'] = str(url_tweet_count)
            data_processed_tweets['spam_url_tweet_count'] = str(spam_url_tweet_count)

            # write data for FILE 3
            with open(file_path_3, 'a') as fp:
                json.dump(data_processed_tweets, fp)
                fp.write(os.linesep)

    def process_user(self, user_id, intersection):
        # process user data

        # get user details
        user = self.get_user(user_id)
        if user == -1:
            return None

        # populate user details for FILE 1
        print "Fetching account details...",
        self.extract_user_details(user)
        print "done!"

        # fetch tweets of chosen user
        print "Fetching tweets...",
        tweets = self.get_tweets(user_id)
        print "done!"

        # populate tweets for FILE 2
        print "Processing tweets...",
        self.extract_tweets(tweets, intersection)
        print "done!"

    def crawl(self, seed):
        # dir path for outputs
        self.dir_path = './fetched/'
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        # begin BFS crawling beginning from a seed user
        seed_user = self.get_user(seed)
        if seed_user == -1:
            print "ERROR: Change Seed User!"
            return None

        # add seed user
        self.users_to_crawl.append(seed_user.id)

        # begin BFS
        account_number = 0
        while len(self.crawled_users) < 10000 and len(self.users_to_crawl) > 0:
            # extract user from list of users to be crawled
            user_id = self.users_to_crawl.pop(0)

            account_number += 1
            print "Processing account", str(account_number) + "..."

            # get users followed by extracted user
            print "Fetching followed...",
            following_list = self.get_following_list(user_id)
            print "done!"

            # get users following the extracted user
            print "Fetching following...",
            followers_list = self.get_followers_list(user_id)
            print "done!"

            # get the intersection of followers and following
            intersecting_users = self.get_intersection_users(following_list, followers_list)

            # add following list users to users-TO-BE-crawled list
            if self.depth > 0 :
                self.add_following(following_list)
                self.depth -= 1

            # process extracted user's data
            self.process_user(user_id, intersecting_users)
            print "=" * 30
            print

            # add processed user to crawled users list
            self.crawled_users[user_id] = 1

        print "-" * 15,
        print str(account_number), "accounts processed",
        print "-" * 15
        print "Goodbye!\n"

    def calculate_probablity(self):
        file_path = self.dir_path + self.processedTweetsFilename
        data = []
        with open(file_path) as f:
            [data.extend(json.loads(line).values()) for line in f]
        computed = []
        for i in data:
            computed.append(self.sigmoid(self.theta*float(i)))
        prob = float(sum(computed))/len(computed) if len(computed) > 0 else float('nan')
        f = open(self.dir_path + self.messageFilename, 'w')
        f.write("Real Account") if prob < 0.5 else f.write("Fake Account")
        f.close()

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))


def main():
    parser = argparse.ArgumentParser()
    requiredArguments = parser.add_argument_group('Required arguments')
    requiredArguments.add_argument('--handle', required=True)
    parser.add_argument('--userfile', default="userinfo.json")
    parser.add_argument('--tweetfile', default="tweetList.json")
    parser.add_argument('--resultfile', default="processedTweets.json")
    parser.add_argument('--probabilityfile', default="probablity.json")
    parser.add_argument("--connections", default="1", type=int)
    parser.add_argument("--depth", default="0", type=int)
    args = parser.parse_args()

    seed = args.handle
    connections = 1

    api_indexes = [i for i in xrange(connections)]

    crawler = TwitterAPI(api_indexes)
    crawler.set_depth(args.depth)
    crawler.set_tweet_filename(args.tweetfile)
    crawler.set_processed_tweets_filename(args.resultfile)
    crawler.set_user_info_filename(args.userfile)
    crawler.set_probability_filename(args.probabilityfile)
    crawler.crawl(seed)
    crawler.calculate_probablity()


if __name__ == '__main__':
    sys.exit(main())
