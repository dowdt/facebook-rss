# Facebook to RSS
Simple python program to turn a facebook account's public posts into an rss feed.
Tried finding something like this online, but none of them seemed ot work.

## Install
```
pip install facebook-scraper
```
For better reliability you should download your facebook cookies into a cookies.json file.
You can use these browser extensions: 
    - for [chrome](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) 
    - for [firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/).


## Usage
Can be run as a python program or script.


Download `accountname`'s posts as a file:
```
facebook2rss.py accountname [options]
```

Download from accounts in config file:
```
facebook2rss.py -c config.txt [options]
```

### Options
```
-c      Path to config file (See README for format)
-j      Path to cookies.json file to be included
-o      Destination directory for rss files (Defaults to working directory)
```


## Config file
Text file with each account name in a newline, with optional nicknames after the comma.

Comment with # and blanklines are ignored.

Example:
```
# here's a simple config
nintendo,Nintendo RSS Feed

xbox,Xbox # Valid comment
GitHub,Nickname for Github
```
