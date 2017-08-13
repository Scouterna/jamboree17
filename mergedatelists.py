#! python

import argparse
import json
import requests
import os
import csv
import uuid

KEY_GROUP_API = os.environ['SCOUTNET_GROUP_KEY']
KEY_PARTICIPANT_API = os.environ['SCOUTNET_PARTICIPANT_KEY'] 

class DuplicateNameError(Exception):
    def __init__(self, message):
        self.message = message


def get_participants():
    r = requests.get('https://183:' + KEY_PARTICIPANT_API +
             '@www.scoutnet.se/api/project/get/participants')
    for key,p in r.json()['participants'].items():
            if(p['group_id'] == None and p['attended'] == True):
            name = p['first_name'] + p['last_name']
            if name in participants:
                raise DuplicateNameError(name)
            participants.add(name)


parser = argparse.ArgumentParser()
args = parser.parse_args()

