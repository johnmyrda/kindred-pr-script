#!/usr/bin/python3
import argparse
from datetime import datetime
import json
import sys

if sys.version_info.major != 3:
    print("This script requires Python 3. Exiting...")
    sys.exit(1)

import urllib.request, urllib.error
# Only standard library modules used in order to maintain broadest possible compatibility
# A more complicated API interaction might warrant usage of the requests library

def parse_command_line():
    parser = argparse.ArgumentParser(description="Get open pull requests and their ages for a given github repo")
    repo_help = "repository name in [user]/[repo] format e.g. apple/swift"
    parser.add_argument("repo", help=repo_help)
    json_output_help = "output as json received from github instead of human readable"
    parser.add_argument("--json-output", action="store_true", help = json_output_help)
    
    # Print help if no arguments specified
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    return args

# Fetch pull requests for a repo using the GitHub v3 API using the urllib module 
def list_pull_requests(repo):
    url = "https://api.github.com/repos/{}/pulls?state=open".format(repo)
    accept_header = {"Accept": "application/vnd.github.v3+json"}
    github_request = urllib.request.Request(url, headers=accept_header)
    try:
        response = urllib.request.urlopen(github_request)
        response_string = response.read()
        json_response = json.loads(response_string)
        return json_response
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print("Error 404 trying to access {}".format(url))
            sys.exit(1)
        else:
            raise

# Format the response to print the PR name and age
# The Pull Request response format is described at https://developer.github.com/v3/pulls/#response        
def print_response(json_response):
    now = datetime.utcnow()
    if len(json_response) > 0:
        for item in json_response:
            created_at = item["created_at"]
            created_at_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            elapsed = now - created_at_datetime
            pr_name = item["title"]
            pr_age = timedelta_human_readable(elapsed)
            print("Name: {}\nAge: {}\n".format(pr_name, pr_age))
    else:
        print("No pull requests found for this repository")

def main():
    args = parse_command_line()
    json = list_pull_requests(args.repo)
    if args.json_output:
        print(json)
    else:
        print("Open pull requests for the {} repository".format(args.repo))
        print("See online at https://www.github.com/{}/pulls".format(args.repo))
        print_response(json)

# takes a timedelta object and returns a human readable string with minute accuracy
# https://docs.python.org/3/library/datetime.html#timedelta-objects
def timedelta_human_readable(delta):
    seconds = int(delta.total_seconds())
    periods =  [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60)
        ]
    time_strings = []
    for period_name, period_length in periods:
        if seconds > period_length:
            period_value = (seconds // period_length)
            seconds = seconds - period_value * period_length
            if period_value > 1:
                unitary_s = 's'
            else:
                unitary_s = ''
            time_strings.append("{} {}{}".format(period_value, period_name, unitary_s))
    return ", ".join(time_strings)

if __name__=="__main__":
    main()