#!/bin/python
import facebook_scraper as fs
import email
import pickle
import sys
import os

def print_help():
    print("""Facebook to RSS converter
If you have issues connecting, importing cookies.json file is recommended.

Usage:
facebook2rss.py <facebook user name> [options]
OR
facebook2rss.py -c <configfile> [options]

Options:
-c      Path to config file (See README for format)
-j      Path to cookies.json file to be included
-o      Destination directory for rss files (Defaults to working directory)
""")

def account_to_rss(profile_name, name='', page_count=2, cookies_file='', dest_folder=''):
    if (name == ''):
        name = profile_name

    print('Downloading ' + profile_name)

    # fs.set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0')

    posts = None
    if cookies_file != '':
        posts = list(fs.get_posts(profile_name, pages=page_count, cookies=cookies_file))
    else:
        posts = list(fs.get_posts(profile_name, pages=page_count))

    print('Finished downloading posts, saving into ' + profile_name + '.xml')
    feed_file = open(os.path.join(dest_folder, profile_name) + '.xml', 'w')
    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    content += '<rss version="2.0">\n'
    content += '<channel>\n'
    content += '<title>' + name + '</title>\n'
    content += '<description>Generated from facebook</description>\n'
    content += '<link> https://facebook.com/' + profile_name + '</link>\n'

    for i, post in enumerate(posts):
        content += '<item>\n'
        content += '\t<title> ' + post['text'] + ' </title>\n'
        content += '\t<link> ' + post['post_url'] + ' </link>\n'
        content += '\t<guid> ' + post['post_url'] + ' </guid>\n'

        content += '\t<description>\n'
        content += '\t\t' + post['text'].replace('&', '&amp;').replace('<','&lt;').replace('>','&gt;') + '\n'
        if post['images'] is not None:
            for img in post['images']:
                content += '\t\t<img src="' + img.replace('&','&amp;') + '"/>'
            content += '\t</description>\n'

            content += '\t<pubDate>' + str(email.utils.format_datetime(post['time'])) + '</pubDate>\n'
            content += '</item>\n'

            print('Saved post ' + str(i + 1) + '/' + str(len(posts)))

        content += '</channel>\n'
        content += '</rss>\n'

    feed_file.write(content)
    feed_file.close()

def main():
    content = ''
    using_config = False
    cookie_file = ''
    using_cookie = False
    dest_folder = ''
    using_custom_dest = False

    if len(sys.argv) < 1:
        print('Invalid, use -h option for help')
        return
    elif '-h' in sys.argv:
        print_help()
        return
    else:
        content = [ sys.argv[1] ]

    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]

        if arg == '-c':
            if i < len(sys.argv) - 1:
                if os.path.isfile(sys.argv[i + 1]):
                    f = open(sys.argv[i + 1], 'r')
                    content = f.readlines()
                    f.close()
                    using_config = True
                    print('found config')
                else:
                    print("Invalid config file")
                    print("use -h option for help")
                    return
            else:
                print("Invalid config argument")
                print("use -h option for help")
                return
        elif arg == '-j':
            if i < len(sys.argv) - 1:
                os.path.isfile
                if os.path.isfile(sys.argv[i + 1]):
                    cookies_file = sys.argv[i + 1]
                    using_cookie = True
                    print('found cookies file')
                else:
                    print("Invalid cookies json file")
                    print("use -h option for help")
                    return
        elif arg == '-o':
            if i < len(sys.argv) - 1:
                if os.path.isdir(sys.argv[i + 1]):
                    dest_folder = sys.argv[i + 1]
                    using_custom_dest = True
                    print('found destination folder')
                else:
                    print("Invalid destination folder")
                    print("use -h option for help")
                    return

    for line in content:
        if len(line) > 3 and line[0] != '#':
            profile_name = line.split('\n')[0].split('#')[0].split(',')
            name = profile_name[0]
            if len(profile_name) == 2:
                name = profile_name[1]
            profile_name = profile_name[0]

            if using_cookie and using_custom_dest:
                account_to_rss(profile_name, name=name, cookies_file=cookies_file, dest_folder=dest_folder)
            elif using_custom_dest:
                print('Importing a cookies file is recommended: ')
                print('Firefox (https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/)')
                print('Chrome  (https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)')
                account_to_rss(profile_name, name=name, dest_folder=dest_folder)
            elif using_cookie:
                account_to_rss(profile_name, name=name, cookies_file=cookies_file)
            else:
                print('Importing a cookies file is recommended: ')
                print('Firefox (https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/)')
                print('Chrome  (https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)')
                account_to_rss(profile_name, name=name)


if __name__ == "__main__":
    main()
