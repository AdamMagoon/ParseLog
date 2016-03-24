#-*- coding: utf-8 -*-

import csv
from os import listdir
from os.path import join
import re
import json
from urllib.request import urlopen
from time import perf_counter

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


class Transfer:
    def __init__(self, ip_address, timestamp, request, response_code,
                 bytes_transfered, referrer, user_agent):
        self.ip_address = ip_address
        self.timestamp = timestamp.split()[0]
        self.request = request
        self.response_code = response_code
        self.bytes_transfered = bytes_transfered
        self.referrer = referrer
        self.user_agent = user_agent

    def __repr__(self):
        return "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(self.ip_address,
                                                   self.timestamp, self.request,
                                                   self.response_code,
                                                   self.bytes_transfered,
                                                   self.referrer,
                                                   self.user_agent)


def parse_transfer_log(file):
    transfers = []

    with open(file, 'r', errors='replace') as f:
            for line in f:
                result = pattern.match(line)
                if result:
                    transfers.append(Transfer(*result.groups()))

    return transfers


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


def display_locations(unique_ips):
    for ip in unique_ips:
        location = get_location_data(ip)
        print("{}, {}, {}  -  {}".format(location['city'], location['regionName'],
                                     location['country'], location['query']))


external_file = r"W:\Web\Backups\Transfer Logs\03202016-transfer.log"
regex = r'([0-9.]+) - - \[(.*)\] "([\w]+ [\S]+ [\S]+|.*)" (\d+) (\d+)?-? "(.*?)" "(.*?)"'
pattern = re.compile(regex)

# unique_req = unique_requests(transfers)
# display_locations(unique_ips)
filters = ['POST']
state_filters = ['New Jersey', 'New Hampshire', 'Massachusetts']

external_dir = 'W:\Web\Backups\Transfer Logs'

files = [join(external_dir, external_file) for external_file in listdir(external_dir)]

for external_file in files:
    transfers = parse_transfer_log(external_file)

    for t in transfers:
        if t.ip_address == '69.164.208.136':
            print(t.ip_address)
            location = get_location_data(t.ip_address)
            with open('unique_ip - log.txt', 'a+', errors='replace') as fi:
                msg = "{} - {}, {}, {}  -  {}  -  {}\n".format(t.timestamp, location['city'], location['regionName'], location['country'], t.ip_address, t.request)
                try:
                    fi.write(msg)
                except UnicodeEncodeError as e:
                    print(e)
                    pass
        # for f in filters:
        #     if f in t.request:
        #         location = get_location_data(t.ip_address)
        #         if location['regionName'] in state_filters:
        #             with open('dump_file2.txt', 'a') as fi:
        #                 msg = "{} - {}, {}, {}  -  {}  -  {}\n".format(t.timestamp, location['city'], location['regionName'], location['country'], t.ip_address, t.request)
        #                 try:
        #                     fi.write(msg)
        #                 except UnicodeEncodeError as e:
        #                     print(e)
        #                     pass

print("Total time: {} seconds".format(perf_counter() - start))




