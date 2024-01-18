#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""
import re
import requests
import sys

def count_words(subreddit, word_list, word_count=[], page_after=None):
    """
    Adds item into a list
    """
    headers = {'User-Agent': 'HolbertonSchool'}

    word_list = [word.lower() for word in word_list]

    if bool(word_count) is False:
        for word in word_list:
            word_count.append(0)

    if page_after is None:
        url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
        r = get(url, headers=headers, allow_redirects=False)
        if r.status_code == 200:
            for child in r.json()['data']['children']:
                j = 0
                for j in range(len(word_list)):
                    for word in [w for w in child['data']['title'].split()]:
                        word = word.lower()
                        if word_list[j] == word:
                            word_count[j] += 1
                    j += 1

            if r.json()['data']['after'] is not None:
                count_words(subreddit, word_list,
                            word_count, r.json()['data']['after'])
    else:
        url = ('https://www.reddit.com/r/{}/hot.json?after={}'
               .format(subreddit,
                       page_after))
        r = get(url, headers=headers, allow_redirects=False)

        if r.status_code == 200:
            for child in r.json()['data']['children']:
                j = 0
                for j in range(len(word_list)):
                    for word in [w for w in child['data']['title'].split()]:
                        word = word.lower()
                        if word_list[j] == word:
                            word_count[j] += 1
                    j += 1
            if r.json()['data']['after'] is not None:
                count_words(subreddit, word_list,
                            word_count, r.json()['data']['after'])
            else:
                dicto = {}
                for key_word in list(set(word_list)):
                    j = word_list.index(key_word)
                    if word_count[j] != 0:
                        dicto[word_list[j]] = (word_count[j] *
                                               word_list.count(word_list[j]))

                for key, value in sorted(dicto.items(),
                                         key=lambda x: (-x[1], x[0])):
                    print('{}: {}'.format(key, value))
