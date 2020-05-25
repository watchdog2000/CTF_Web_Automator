# CTF_Web_Automator
A small and simple program to aid within web recon in a CTF.

This tool can scrape a site for all HTML comments, as well as ‘flags’ both inside and outside of comments. This automated and aids in extracting potential usernames, passwords, helpful hints, and flags of a specific format from web pages.

It accepts a parameter to be able to visit any webpages previously found using tools such as gobuster or dirbuster, as well as spidering in runtime to find links to other standard pages on the site not picked up from your previous recon. 

The only dependency is python3, and the requests module is installed: 'python3 -m pip install requests'.

USAGE: 
'python3 web-source-extractor.py -u < url > -p < file containing a list of page sub directories > -f < hex | fixed-length | custom >'

EXAMPLE:
'python3 web-source-extractor.py -u http://test.com/ -p pages-found.txt -f fixed-length:32'

HELP:



