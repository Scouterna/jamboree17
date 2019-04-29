#! python
# coding=utf-8

# Uses Scoutnet's activity checkin API to update chekin details using a csv list, allowing for offline updates
# on a field with shaky Internet connection.
import argparse
import json
import requests
import os
import csv
import uuid
import re

KEY_CHECKIN_API = os.environ['SCOUTNET_CHECKIN_API']


parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Weird csv file with member numbers and status")
parser.add_argument("comment", help="Comment to amend to all checkins/outs")
args = parser.parse_args()


with open(args.infile) as f:
    r = csv.DictReader(f, dialect='excel', delimiter=',')
    for row in r:
        ret = {str(row['Medlemsnummer']):{'checked_in':str(row['Incheckad']),
                                          'comment':args.comment}
              }
        post = requests.post('https://www.scoutnet.se/api/project/checkin',
                             params={'id':'183','key':KEY_CHECKIN_API},
                             headers={'Content-Type':'application/json'},
                             json=ret)

