#!/usr/bin/python

import csv
import datetime
import os
import sys

if __name__ == '__main__':
    cur_file = os.path.abspath(__file__)
    django_dir = os.path.abspath(os.path.join(os.path.dirname(cur_file), '..'))
    sys.path.append(django_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import connection
from django.db.models import Q
from django.utils import html

import groups.models
import space.models

def space_Q(merged_acl=None, building=None, ):
    Qspace = Q()
    if merged_acl is not None: Qspace = Q(space__merged_acl=merged_acl)
    if building: Qspace = Qspace & Q(space__number__startswith=building+'-')
    return Q(spaceassignment__in=space.models.SpaceAssignment.current.filter(Qspace))

Qsa = Q(group_status__slug__in=('active', 'suspended', ))

functions = {
    'finboard' : {
        'format' : "%(name)s;%(officer_email)s",
        'predicate' : Qsa & Q(group_funding__slug='undergrad', group_class__slug='mit-funded', ),
    },
    'nolist' : {
        'format' : "%(name)s <%(officer_email)s>",
        'predicate' : Qsa & Q(officer_email=""),
    },
    'asa-official' : {
        'format' : '"%(name)s" <%(officer_email)s>',
        'predicate' : Q(group_status__slug='active'),
    },
    'emails-only' : {
        'format' : '%(officer_email)s',
        'predicate' : Qsa,
    },
    'midway' : {
        'prefix': """
        <!--
        Automatically generated by %(script)s %(mode)s on %(date)s.
        Do not edit; instead ask a DB maintainer (asa-db@) to re-run that script (or edit script as necessary).

        A more recent version may be in /mit/asa-db/data/db-dump/midway_groups.html.
        Includes active, suspended, applying, and NGE's (status) who aren't Dorm/FSILG (class).
        -->
        """,
        'format' : '<option value="%(html_name)s">%(html_name)s</option>',
        'predicate' : Q(group_status__slug__in=['active', 'suspended', 'applying', 'nge'], group_class__gets_publicity=True, ),
    },
    'w20-locker' : {
        'format' : '%(officer_email)s;%(name)s',
        'predicate' : Qsa & space_Q(merged_acl=True, building='W20'),
    },
    'w20-office' : {
        'format' : '%(officer_email)s;%(name)s',
        'predicate' : Qsa & space_Q(merged_acl=False, building='W20'),
    },
    'all-office' : {
        'format' : '%(officer_email)s;%(name)s',
        'predicate' : Qsa & space_Q(merged_acl=False),
    },
    'all-space' : {
        'format' : '%(officer_email)s;%(name)s',
        'predicate' : Qsa & space_Q(),
    },
}

def do_output(mode):
    spec = functions[mode]
    format = spec['format']
    predicate = spec['predicate']
    gs = groups.models.Group.objects.filter(predicate).distinct()
    static_args = {
        'script': 'groups/format_groups.py',
        'mode':mode,
        'date':datetime.datetime.now(),
    }
    if 'prefix' in spec:
        print spec['prefix'] % static_args
    for group in gs:
        print format % {
            'name':group.name,
            'html_name':html.escape(group.name),
            'officer_email':group.officer_email,
        }
    if 'suffix' in spec:
        print spec['suffix'] % static_args
    #for q in connection.queries: print q

if __name__ == "__main__":
    do_output(sys.argv[1])
