#!/bin/python
import facebook_scraper
from facebook_scraper import get_posts
import email
import pickle
import sys

def print_help():
    print(""" 
Facebook to RSS

-h for help
-c for config file
""")

def main():

    sys.argv

    f = open('config', 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        if len(line) > 3 and line[0] != '#':
            profile_name = line.split('#')[0].split('\n')[0]
            name = profile_name

            if len(profile_name.split(',')) == 2:
                profile_name = profile_name.split(',')[0]
                name = profile_name.split(',')[1]

            feed_file = open(profile_name + '.xml', 'w')
            print('downloading ' + profile_name + '.xml')


            # posts = list(get_posts(profile_name, pages=1, cookies="cookies.json"))
            p_f = open('savedposts.pickle', 'rb')
            posts = list(pickle.load(p_f))
            p_f.close()

            # p_f = open('savedposts.pickle', 'wb')
            # pickle.dump(posts, p_f)
            # p_f.close()

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


if __name__ == "__main__":
    main()
