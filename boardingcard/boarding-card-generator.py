import jinja2
import json
import requests
import os
import uuid
from jinja2 import Template

KEY_GROUP_API = os.environ['SCOUTNET_GROUP_KEY']
KEY_PARTICIPANT_API = os.environ['SCOUTNET_PARTICIPANT_KEY'] 

latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)


def get_groups():
    r = requests.get('https://183:' + KEY_GROUP_API +
             '@www.scoutnet.se/api/project/get/groups?flat=true')
    return r.json()


def get_participants():
    r = requests.get('https://183:' + KEY_PARTICIPANT_API +
             '@www.scoutnet.se/api/project/get/participants')
    return r.json()['participants']


def get_key_participant_tuple(item):
    return item[0]

groups = {}
for id,group in get_groups().items():
    g = group
    g['id'] = id.zfill(7)
    g['participants'] = []
    groups[id] = g

for id,participant in get_participants().items():
    if(participant['group_registration']==True and
       participant['cancelled']==False):
        name=participant['last_name'] + ', ' + participant['first_name']
        groups[str(participant['group_id'])]['participants'].append(
                                               (name, participant['member_no']))

template = latex_jinja_env.get_template('template.tex')

for id,group in groups.items():
    tex = template.render(group_id=group['id'], group_name=group['name'],
                          village=group['questions']['820'],
                          group_no=group['group_no'],
                          group_participant_no=group['group_participants'],
                          participants=sorted(group['participants'],
                                              key=get_key_participant_tuple))

    uniqueid=str(uuid.uuid1())
    filename = str(group['group_no']) + '-' + uniqueid

    with open('output/' + filename + '.tex','w') as f :
        f.write(tex)

    print(str(group['group_no']) + ','+str(group['id'])+','+uniqueid)
