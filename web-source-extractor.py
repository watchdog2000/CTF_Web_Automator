"""
web-source-scraper.py - automating web recon
author: watchdog2000
24/05/2020
python3 web-source-scraper.py --url <url> --flag-format <hex|length|custom>
(if custom then prompt for first few chars and last char/chars if known)
"""
import optparse   # for arg parsing
import requests  # for the requests sent
import re  # regex
import sys  # system commands

pages = []
all_comments = []
all_flags = []


#  argument handling
def arg_parsing():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest='url',
                      help='[REQUIRED] - The site which you wish to scrape '
                      'for html comments')
    parser.add_option('-f', '--flag-format', dest='flag_format',
                      help='[OPTIONAL] - The format for any flags you wish to '
                      'scrape from the site.\n[hex|custom]')
    parser.add_option('-p', '--pages', dest='pages',
                      help='[OPTIONAL] - a file containing a list of '
                      'directories of additonal pages on the site (recommended'
                      ' to dir-bust before to find pages to scrape)')
    (args, options) = parser.parse_args()
    return (args, options)


#  accept url as a param and validate it being a website format
def url_check(url):
    valid_url = re.compile('http(s)?://\w+\.\w+\S*')
    if url and valid_url.match(url):
        if url.endswith('/'):
            url = url[:len(url) - 1]
        return url
    else:
        print('[-] - ERROR - Please enter a valid URL: ' +
              'http(s)://www.example.com/example', file=sys.stderr)
        sys.exit(0)


def flag_format_check(flag_format_option):
    # setting up the handling of flags
    flag_format = ''
    if flag_format_option:
        flag_format = flag_format_option.lower()
        if flag_format == 'hex':
            flag_format = "[0-9a-fA-F]{2,}"
        elif flag_format == 'custom':
            while True:
                first_chars = input('[?] - What are the first few characters '
                                    'of your flag?\n')
                if first_chars:
                    while True:
                        last_chars = input('[?] - What are the last known '
                                           'characters of your flag?\n')
                        if last_chars:
                            break
                        else:
                            print('[-] - Please enter something')
                    break
                else:
                    print('[-] - Please enter something')
            flag_format = first_chars + '\S+?' + last_chars
            return flag_format
        else:
            print('[-] - ERROR - Please enter \'hex\', \'fixed-length\'\, \or '
                  '\'custom\' ONLY', file=sys.stderr)
            sys.exit(0)


#  read in dirs to access and scrape from file
def pages_read(page_file):
    # reads pages to visit from the supplied document
    pages = ['/']
    if page_file:
        with open(page_file, 'r') as f:
            for page in f:
                pages.append(page.strip())
    return pages


def print_sep(num_chars):
    print('   ' + '-' * num_chars + ' \n')


def print_summary(all_flags, all_comments, pages):
        # printing summary
        print_sep(35)
        if all_flags or all_comments:
            print('[*] -- SUMMARY -- [*]')
            print(f"[+] - {len(pages)} Pages scraped...\n")
            [print('    - ' + page + '\n') for page in pages]
        if all_comments:
            print('-- HTML COMMENTS --')
            [print('    - ' + comment + '\n') for comment in all_comments]
        if all_flags:
            print('\n-- FLAGS --')
            [print('    - ' + flag + '\n') for flag in all_flags]


def main():
    # initialising
    (args, options) = arg_parsing()
    url = url_check(args.url)
    flag_format = flag_format_check(args.flag_format)
    pages = pages_read(args.pages)

    all_comments = []
    all_flags = []

    # regex for html comments
    html_comment = re.compile('<!--(?:.|\r|\n)+?-->')
    # regex for finding links to other pages
    find_href = re.compile("href=\".+?\"")

    # implement checking that the initial url can be reached to avoid erroring
    try:
        print(f'\n[*] - Connecting to {url}...\n')
        r = requests.get(url)
    except:
        print(f'[-] - ERROR - Connection to {url} could not be made',
              file=sys.stderr)
        sys.exit(0)

    # iterate through pages to find data
    index = 1
    for page in pages:
        r = requests.get(url+page)
        page_data = r.text

        print_sep(35)
        print(f"[*] - Page {index} out of {len(pages)} - [*]")
        index += 1
        print(f'[*] - {url+page} - [*]')
        if page_data:
            print(f'[+] - HTML RESPONSE - ' + str(r.status_code))
        else:
            print(f'[-] - {url} did not respond well to that request... sorry')
            continue

        # extracting html comments
        comments = re.findall(html_comment, page_data)
        if comments:
            print('\n[+] - COMMENTS - [+]')
            for comment in comments:
                print('- \"' + comment + '\"\n')
                if comment not in all_comments:
                    all_comments.append(comment)
        else:
            print('[-] - No HTML comments present\n')

        # tests for lower case,  upper case, and title case flag to be thorough
        if flag_format:
            flags = re.findall(flag_format, page_data)
            flags += re.findall(flag_format.upper(), page_data)
            flags += re.findall(flag_format.title(), page_data)

            if flags:
                print('[+] - FLAGS - [+]\n')
                for flag in flags:
                    print('- ' + flag + '\n')
                    if flag not in all_flags:
                        all_flags.append(flag)
            else:
                print('[-] - No flags found...')

        # finding new pages to spider
        links = re.findall(find_href, page_data)
        for link in links:
            link = link[len('href="'):-1]

            if url in link:
                link = link[len(url):]

            if link not in pages and link.startswith('/'):
                pages.append(link)

    print_summary(all_flags, all_comments, pages)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[-] - Keyboard Interrupt - Exiting')
        sys.exit(0)
