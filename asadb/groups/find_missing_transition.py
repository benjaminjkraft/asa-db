#!/usr/bin/python
import csv
import os
import sys

if __name__ == '__main__':
    cur_file = os.path.abspath(__file__)
    django_dir = os.path.abspath(os.path.join(os.path.dirname(cur_file), '..'))
    sys.path.append(django_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core import mail
from django.template import Context, Template
from django.template.loader import get_template

import groups.models

def get_roles():
    roles = [
        ['treasurer', 'No treasurer listed', ],
        ['financial', 'No financial signatories listed. At minimum, this should generally be your president and treasurer.', ],
        ['reservation', 'No reservation signatories listed. Members reserving space for the group should be reservation signatories.', ],
    ]
    for role in roles:
        obj = groups.models.OfficerRole.objects.get(slug=role[0])
        role[0] = obj
    return roles

def check_group(group, roles, ):
    problems = []
    if group.officer_email or group.description:
        pass
    else:
        problems.append("No basic group information listed")
    for role, msg in roles:
        if len(group.officers(role=role)) == 0:
            problems.append(msg)
    return problems

def officers_lists(fd, ):
    reader = csv.DictReader(fd)
    lists = {}
    for d in reader:
        pk = int(d['ASA_STUDENT_GROUP_KEY'])
        lists[pk] = d['OFFICER_EMAIL']
    return lists

def check_groups(old_groups_data):
    roles = get_roles()
    officers = officers_lists(open(old_groups_data, 'r'))
    tmpl = get_template('groups/letters/missing-transition.txt')
    emails = []
    for group in groups.models.Group.active_groups.all():
        problems = check_group(group, roles, )
        if problems:
            to = [officers[group.pk]]
            if group.officer_email:
                to.append(group.officer_email)
            ctx = Context({
                'group': group,
                'problems': problems,
            })
            body = tmpl.render(ctx)
            email = mail.EmailMessage(
                subject="[ASA] Missing information for %s" % (group.name, ),
                body=body,
                from_email='asa-exec@mit.edu',
                to=to,
                bcc=['asa-admin@mit.edu' , 'asa-db-outgoing@mit.edu'],
            )
            emails.append(email)

    connection = mail.get_connection()
    connection.send_messages(emails)

if __name__ == '__main__':
    check_groups(sys.argv[1])
