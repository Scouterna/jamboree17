#! python

import argparse
import json
import requests
import os
import csv
import uuid

KEY_GROUP_API = os.environ['SCOUTNET_GROUP_KEY']
KEY_PARTICIPANT_API = os.environ['SCOUTNET_PARTICIPANT_KEY'] 


def get_participants():
    r = requests.get('https://183:' + KEY_PARTICIPANT_API +
             '@www.scoutnet.se/api/project/get/participants')
    return r.json()['participants']


parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Weird csv file with volunteer dates")
args = parser.parse_args()


participants = {}


with open(args.infile) as f:
    r = csv.reader(f, dialect='excel')
    for row in r:

