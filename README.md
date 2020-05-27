# CTF_Web_Automator
A small and simple program to aid with web recon within a CTF competition.

This tool can scrape a site for all HTML comments, as well as ‘flags’ both inside and outside of comments. This automated and aids in extracting potential usernames, passwords, helpful hints, and flags of a specific format from web pages.

It accepts a parameter to be able to visit any webpages previously found using tools such as gobuster or dirbuster, as well as spidering in runtime to find links to other standard pages on the site not picked up from your previous recon. 

The only dependency is python3, the requests module and the optparse module (which, while deprecated to favour argparse, is preffered by myself): 'python3 -m pip install requests optparse'.

USAGE:

'python3 web-source-extractor.py -u <url> -p <file containing a list of page sub directories> -f <hex | regex | custom>'

EXAMPLE:

'python3 web-source-extractor.py -u http://thisisatest.com/ -p pages-found.txt -f hex'

The file containing web directories that you wish to scrape should be a list, with each directory starting with a '/' and on a new line:

'/home

/blogs

/test'

The flag format can currently be hexadecimal, a regex string or a custom format, where the user is prompted for the first know character or charcaters, and the last known character or characters. Flag formats are often like: 'FLAG{<flag here>}' so the user would input 'FLAG{' and '}'. Of course, the more characters you input, the more accurate the tool will be, wih less false positives.
  
It goes without saying, make sure you have permission/aren't in breach of terms of service for any websites you scrape for this data.
