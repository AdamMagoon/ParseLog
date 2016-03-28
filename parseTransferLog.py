#-*- coding: utf-8 -*-

"""
    Initial Run-time
    2.35 Hours
    141.2 Minutes

"""

from os import listdir
from os.path import join
import re
import json
from urllib.request import urlopen
from time import perf_counter
from models import Transfer, CustomerTracker

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


# Must use full state names
data_source = 'W:\Web\Backups\Transfer Logs'
state_filters = ['New Jersey', 'New Hampshire', 'Massachusetts']

# Tracking data
ip_count = {}  # Counts how many times an IP address shows up


# Compile data_source log info into line-by-line class instances
def compile_logs_into_customers(data_source):
    track_customers = {}  # Saves class instances of CustomerTracker class based on IP address
    files = [join(data_source, external_file) for external_file in listdir(data_source)]

    for file in files:
        log_entries = parse_dsa_website_transfer_log(file)

        for log in log_entries:  # log = Transfer() instance

            # If IP Address exists within dict, add Transfer instance to value
            if log.ip_address in track_customers:
                track_customers[log.ip_address].add_log(log)

            # Else create a CustomerTracker instance and add it to the key's value
            else:
                customer = CustomerTracker(log.ip_address)
                customer.add_log(log)
                track_customers[log.ip_address] = customer

    return track_customers

track_customers = compile_logs_into_customers(data_source)

login_count = 0

for user in track_customers.values():
    if len(user.login_instances) > 0:
        login_count += 1
        print(user)

print("Total Users That Logged In: {}".format(login_count))

print("Total time: {} seconds".format(perf_counter() - start))
