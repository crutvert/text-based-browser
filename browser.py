import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
init()


def check_url(url):
    if '.' in url:
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = 'http://' + url
        try:
            r = requests.get(url)
            return r.content
        except Exception:
            return False
    else:
        return False

def html_to_text(site_reply):
    soup = BeautifulSoup(site_reply, 'html.parser')
    tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    paragraphs = soup.find_all(tags)
    site_text = ''
    for el in paragraphs:
        if el.name == 'a':
            site_text += Fore.BLUE + el.text + Fore.RESET + '\n'
        else:
            site_text += el.text + '\n'
    return site_text


def write_to_file(cache_dir, url, text):
    global cache
    short = short_name(url)
    cache[url] = short
    with open(cache_dir + '\\' + short, 'w') as f:
        print(text, file=f)


def read_from_cache(cache_dir, url):
    with open(cache_dir + '\\' + url, 'r') as f:
        for el in f:
            print(el.rstrip('\n'))


def short_name(url):
    parse = url.split('.')
    file_name = parse[0]
    if len(parse) > 2:
        for el in range(1, len(parse) - 1):
            file_name += '.' + parse[el]
    return file_name


save_dir = ''
history = deque()
previous = ''
cache = dict()
if len(sys.argv) > 1:
    save_dir = sys.argv[1]
    if os.path.isdir(save_dir):
        pass
    else:
        os.mkdir(save_dir)
while True:
    user_in = input()
    if user_in == 'exit':
        exit()
    elif user_in == 'back':
        if history and save_dir != '':
            read_from_cache(save_dir, cache[history.pop()])
    else:
        if save_dir != '' and user_in in cache.values():
            read_from_cache(save_dir, user_in)
        elif user_in not in cache:
            reply = check_url(user_in)
            if reply:
                site_data = html_to_text(reply)
                print(site_data)
                if save_dir != '':
                    if previous != '':
                        history.append(previous)
                    previous = user_in
                    write_to_file(save_dir, user_in, site_data)
            else:
                print("Error: Incorrect URL")
        else:
            print("Error: Incorrect URL")
