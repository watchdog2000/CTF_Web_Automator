"""
web-source-scraper.py - automating web recon
author: watchdog2000
24/05/2020
python3 web-source-scraper.py --url <url> --flag-format <hex|length|custom>
(if custom then prompt for first few chars and last char/chars if known)
"""
import optparse
import requests
import re
import sys

# argument handling
parser = optparse.OptionParser()
parser.add_option('-u', '--url', dest='url',
                help='[REQUIRED] - The site which you wish to scrape for html \
                comments')
parser.add_option('-f', '--flag-format', dest='flag_format',
                help='[OPTIONAL] - The format for any flags you wish to scrape \
                from the site.\n[hex|fixed-length|custom]')
parser.add_option('-p', '--pages', dest='pages',
                help='[OPTIONAL] - a file containing a list of directories of \
                additonal pages on the site (recommended to dir-bust before to \
                find pages to scrape)')
(args, options) = parser.parse_args()

# accept url as a param and validate it being a website format
valid_url = re.compile('http(s)?://\w+\.\w+.*')
if args.url and valid_url.match(args.url):
    url = args.url
    if url.endswith('/'):
        url = url[:len(url) - 1]
else:
    print('[-] - ERROR - Please enter a valid URL: ' +
    'http(s)://www.example.com/example', file=sys.stderr)
    sys.exit(1)

flag_format = ''
if args.flag_format:
    flag_format = args.flag_format.lower()
    if flag_format == 'hex':
        pass # set up hex regex.
    elif flag_format == 'fixed-length':
        pass # set up length regex
    elif flag_format == 'custom':
        pass # prompt for more info - first known chars for beginning, last known chars for end
    else:
        print('[-] - ERROR - Please enter \'hex\', \'fixed-length\'\, \or '
        '\'custom\' ONLY', file=sys.stderr)
        sys.exit(1)

# read in dirs to access and scrape from file
pages = ['/']
if args.pages:
    with open(args.pages, 'r') as f:
        for page in f:
            pages.append(page.strip())

#regex for html comments
html_comment = re.compile('<!--(?:.|\r|\n)+-->')

# implement checking that the url can be reached to avoid erroring
try:
    print(f'\n[*] - Connecting to {url}...\n')
    page_data = requests.get(url).text
except:
    print(f'[-] - ERROR - Connection to {url} could not be made',
    file=sys.stderr)
    sys.exit(1)

for page in pages:
    page_data = requests.get(url+page).text
    print('   ' + '-'*35 +' \n')
    print(f'[*] - {url+page} - [*]')
    if page_data:
        print(f'[+] - Successful html response')
    else:
        print(f'[-] - {url} did not respond well to that request... sorry')
        continue

    # extracting data
    comments = re.findall(html_comment, page_data)
    if comments:
        print('\n[+] - COMMENTS - [+]')
        for comment in comments:
            if len(comment) < 100:
                # sometimes pages start and end with a comment,
                # so the whole page is picked up as a comment
                print('- \"' + comment + '\"\n')
            else:
                print('[-] - Comment exceeded 100 chars in length...' +
                f'page starts and ends with comments? Check out {url+page}\n')
    else:
        print('[-] - No HTML comments present\n')

    # tests for lower case,  upper case, and title case flag - just to be thorough
    if flag_format:
        flags = re.findall(flag_format, page_data)
        flags += re.findall(flag_format.upper(), page_data)
        flags += re.findall(flag_format.title(), page_data)

        if flags:
            print('[+] - FLAGS - [+]\n')
            for flag in flags:
                print('- ' + flag + '\n')
        else:
            print('[-] - No flags found...')
