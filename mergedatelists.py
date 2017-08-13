#! python

import argparse
import json
import requests
import os
import csv
import uuid
import re

KEY_GROUP_API = os.environ['SCOUTNET_GROUP_KEY']
KEY_PARTICIPANT_API = os.environ['SCOUTNET_PARTICIPANT_KEY'] 

class DuplicateNameError(Exception):
    def __init__(self, message):
        self.message = message


def get_participants():
    participants = {}
    r = requests.get('https://183:' + KEY_PARTICIPANT_API +
             '@www.scoutnet.se/api/project/get/participants')
    for key,p in r.json()['participants'].items():
            if(p['group_id'] == None and p['attended'] == True):
                name = p['first_name'] + p['last_name']
                if name in participants.keys():
                    raise DuplicateNameError(name)
                participants[name] = p
    return participants


parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Weird csv file with volunteer dates")
args = parser.parse_args()


participants = get_participants()


with open(args.infile) as f:
    r = csv.DictReader(f, dialect='excel', delimiter=';')
    print(r.fieldnames)
    for row in r:
        key = ''.join(filter(str.isalpha,row['Namn']))
        ret = {'checked_in': True, 'attended': True, 'questions':{}}
        for i in range(7,16):
            print(str(i) + ' ' + row[str(i)+'/8'])
            if (row[str(i)+'/8']=='1'):
                # First date question has number 800 
                ret['questions'][str(i+799)] = 1
            elif (row[str(i)+'/8'] is None):
                ret['questions'][str(i+799)] = 0
            elif (row[str(i)+'/8'] == 'M'):
                ret['questions'][str(i+799)] = 1
                ret['questions']['941'] = "20:00"
            elif (row[str(i)+'/8'] == 'L'):
                ret['questions'][str(i+799)] = 1
                ret['questions']['941'] = "14:00"
            elif (row[str(i)+'/8'] == 'F'):
                ret['questions'][str(i+799)] = 1
                ret['questions']['941'] = "10:00"
        print(ret)
