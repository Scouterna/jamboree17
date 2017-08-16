#! python
# coding=utf-8

import argparse
import json
import requests
import os
import csv
import uuid
import re

KEY_GROUP_API = os.environ['SCOUTNET_GROUP_KEY']
KEY_PARTICIPANT_API = os.environ['SCOUTNET_PARTICIPANT_KEY'] 
KEY_CHECKIN_API = os.environ['SCOUTNET_CHECKIN_KEY']

class DuplicateNameError(Exception):
    def __init__(self, message):
        self.message = message


def get_participants():
    participants = {}
    r = requests.get('https://www.scoutnet.se/api/project/get/participants',
                     params={'id':183, 'key':KEY_PARTICIPANT_API})
    for key,p in r.json()['participants'].items():
            if(p['group_id'] == None):
                name = ''.join(filter(is_swedish_alpha,
                                    p['first_name'] + p['last_name']))
                if name in participants.keys():
                    pass
                    #raise DuplicateNameError(name)
                participants[name] = p
    return participants

def is_swedish_alpha(character):
    return(character in
           "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖabcdefghijklmnopqrstuvwxyzåäö")

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Weird csv file with volunteer dates")
args = parser.parse_args()


participants = get_participants()


with open(args.infile) as f:
    r = csv.DictReader(f, dialect='excel', delimiter=';')
    print(r.fieldnames)
    for row in r:
        key = ''.join(filter(is_swedish_alpha,row['Namn']))
        updates = {'questions':{}}
        for i in range(7,17):
            if (row[str(i)+'/8']=='1'):
                # First date question has number 800 
                updates['questions'][str(i+793)] = {'value':'1'}
            elif (row[str(i)+'/8'] is None):
                updates['questions'][str(i+793)] = {'value':'1'}
            elif (row[str(i)+'/8'] == 'M'):
                updates['questions'][str(i+793)] = {'value':'1'}
                updates['questions']['941'] = {'value':"20:00"}
            elif (row[str(i)+'/8'] == 'L'):
                updates['questions'][str(i+793)] = {'value':'1'}
                updates['questions']['941'] = {'value':"14:00"}
            elif (row[str(i)+'/8'] == 'F'):
                updates['questions'][str(i+793)] = {'value':'1'}
                updates['questions']['941'] = {'value':"10:00"}
        try:
            ret = {participants[key]['member_no']:updates}
        except KeyError:
            print(key)
        post = requests.post('https://www.scoutnet.se/api/project/checkin',
                             params={'id':'183','key':KEY_CHECKIN_API},
                             headers={'Content-Type':'application/json'},
                             json=ret)
