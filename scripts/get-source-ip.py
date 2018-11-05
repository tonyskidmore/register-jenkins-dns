#!/usr/bin/env python

"""
Oct 2018, Tony Skidmore <anthony.skidmore@accenture.com>

Simple script to attempt to retrieve source IP address for use
in firewall rules or security groups.  If ip address is determined
then it will be returned else nothing will be returned.
"""
from __future__ import print_function

try:
    from requests import get
    from requests.exceptions import RequestException
    import sys
    import re

    HAS_MODULES = True

except ImportError:
    HAS_MODULES = False

if not HAS_MODULES:
    sys.exit(1)

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with get(url, stream=True) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        # turn off any ouputs other than ip address
        # log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_ip_address(text_str):
    """
    extract ip address from response using regex
    """

    regex = r"([0-9]{1,3}\.?){4}"

    matches = re.finditer(regex, text_str, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

    if matchNum == 1:
        match = match.group()
    else:
        match = None

    return match


def main(args):
    """ main function """

    url = 'http://checkip.dyndns.org'

    response = simple_get(url)

    if response:
        ip_address = get_ip_address(response)

    if 'ip_address' in locals():
        print(ip_address)

if __name__ == '__main__':
    main(sys.argv[1:])