#-*- coding: utf-8 -*-

"""
    Initial Run-time
    2.35 Hours
    141.2 Minutes

"""

import csv
from os import listdir as ld
from os.path import join
import re
import json
from urllib.request import urlopen
from time import perf_counter
from models import Transfer

start = perf_counter()


def get_location_data(ip_address):
    """
        ip address = 'query'
        'regionName'
        'countryCode'
        'city'
        'country'
        'region'
        'timezone'
    """
    api = 'http://ip-api.com/json/{}'.format(ip_address)
    response = urlopen(api)
    str_response = response.readall().decode('utf-8')
    location_object = json.loads(str_response)

    return location_object


def parse_dsa_website_transfer_log(file):
    """
        Custom function to parse Nexcess Apache server transfer logs
        and return a list of Transfer class objects
    """
    regex = r'([0-9.]+) - - \[(.*)\] "([\w]+ [\S]+ [\S]+|.*)" (\d+) (\d+)?-? "(.*?)" "(.*?)"'
    pattern = re.compile(regex)
    log_entries = []

    with open(file, 'r', errors='replace') as f:
            for line in f:
                result = pattern.match(line)
                if result:
                    log_entries.append(Transfer(*result.groups()))

    return log_entries


def unique_requests(transfers):
    requests = set()
    for log in transfers:
        if log.request not in requests:
            requests.add(log.request)
    return requests


def unique_ip_addresses(transfers):
    unique_ips = set()
    for log in transfers:
        if log.ip_address not in unique_ips:
            unique_ips.add(log.ip_address)
    return unique_ips


def locations_from_ips(unique_ips):
    """
        Accepts a list of ip addresses and returns a list of
        formatted strings
    """
    loc_list = []
    for ip in unique_ips:
        loc = get_location_data(ip)
        formated = "{}, {}, {}  -  {}".format(loc['city'], loc['regionName'],
                                     loc['country'], loc['query'])
        loc_list.append(formated)

    return loc_list


def location_from_ip(ip_address):
    """
        Accepts an ip addresses as a string and returns a formatted string
    """

    loc = get_location_data(ip_address)
    formated = "{}, {}, {}".format(loc['city'], loc['regionName'],
                                 loc['country'])

    return formated


state_filters = ['New Jersey', 'New Hampshire', 'Massachusetts']
external_dir = 'W:\Web\Backups\Transfer Logs'
files = [join(external_dir, external_file) for external_file in ld(external_dir)]

# Most common ip addresses with counts
ip_count = {}
unique_post_requests = set()
for file in files:
    log_entries = parse_dsa_website_transfer_log(file)

    for log in log_entries:

        if log.ip_address in ip_count:
            ip_count[log.ip_address] += 1
        else:
            ip_count[log.ip_address] = 1

        if 'POST' in log.request:
            unique_post_requests.add(log.request)

with open('posts_and_ipcounts.txt', 'a', errors='replace') as f:
    f.write("Unique Post Requests and IP Address Counts\n")

    for post in unique_post_requests:
        post = post.split()[1]
        f.write(post + '\n')

    f.write('\n')
    sorted_ip_counts = ((k, ip_count[k]) for k in sorted(ip_count, key=ip_count.get, reverse=True))
    i = 0
    for k, v in sorted_ip_counts:
        loc = location_from_ip(k)
        f.write("{} - {} - {}\n".format(v, k, loc))
        i += 1
        print(i)

print("Total time: {} seconds".format(perf_counter() - start))
