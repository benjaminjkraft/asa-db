# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

import sys

officerroles = [
    ('President', 'president', 'The president (which sometimes goes by names like "Chair", "Governor", or "Commander") is ultimately responsible for a group\'s operations.', 2, True, 'groupadmin@SYSTEM', True, ),
    ('Treasurer', 'treasurer', 'The Treasurer is the officer responsible for the group\'s finances.', 2, True, 'groupadmin@SYSTEM', True, ),
    ('Financial signatory', 'financial', 'Financial signatories handle the group\'s financial transactions, including approving RFPs, requesting purchase orders, and viewing transaction history.', 6, False, None, True, ),
    ('Reservation signatory', 'reservation', 'Reservation signatories are responsible for reserving space for the group to use.', 10000, False, None, True, ),
    ('Office access', 'office-access', 'People able to use their IDs to get into the offices of this group.', 10000, False, None, False, ),
]

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        self.migrate_officerroles_forwards(orm, officerroles, )


    def backwards(self, orm):
        "Write your backwards methods here."
        # We probably don't want to do this, since it's liable to delete the
        # prob signatory records by mistake someday...
        #self.migrate_officerroles_backwards(orm, officerroles, )
        print "Refraining from removing OfficerRoles."


    def migrate_officerroles_forwards(self, orm, officerroles, ):
        for officerrole_tuple in officerroles:
            defaults = {}
            defaults['display_name'], slug, defaults['description'], defaults['max_count'], defaults['require_student'], grant_user, defaults['publicly_visible'] = officerrole_tuple
            if grant_user:
                defaults['grant_user'] = orm['auth.user'].objects.get(username=grant_user)
            officerrole, created = orm['groups.officerrole'].objects.get_or_create(slug=slug, defaults=defaults)

    def migrate_officerroles_backwards(self, orm, officerroles, ):
        for officerrole_tuple in officerroles:
            slug = officerrole_tuple[1]
            try:
                orm['groups.officerrole'].objects.get(
                    slug=slug,
                ).delete()
            except orm['groups.officerrole'].DoesNotExist:
                print >>sys.stderr, "OfficerRole %s does not exist while backwards migrating adding it." % (slug, )

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'groups.activitycategory': {
            'Meta': {'object_name': 'ActivityCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'groups.athenamoiraaccount': {
            'Meta': {'object_name': 'AthenaMoiraAccount'},
            'account_class': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'add_date': ('django.db.models.fields.DateField', [], {}),
            'del_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'mit_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mutable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'groups.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'activity_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.ActivityCategory']", 'null': 'True', 'blank': 'True'}),
            'advisor_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'athena_locker': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'constitution_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'funding_account_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.GroupClass']"}),
            'group_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'group_funding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.GroupFunding']", 'null': 'True', 'blank': 'True'}),
            'group_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.GroupStatus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_account_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_times': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'num_community': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_grads': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_other': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_undergrads': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'officer_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'recognition_date': ('django.db.models.fields.DateField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updater': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'groups.groupclass': {
            'Meta': {'object_name': 'GroupClass'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'gets_publicity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'groups.groupfunding': {
            'Meta': {'object_name': 'GroupFunding'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'funding_list': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'groups.groupnote': {
            'Meta': {'object_name': 'GroupNote'},
            'acl_read_group': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'acl_read_offices': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'groups.groupstartup': {
            'Meta': {'object_name': 'GroupStartup'},
            'create_athena_locker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'create_group_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'create_officer_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'president_kerberos': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'president_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stage': ('django.db.models.fields.IntegerField', [], {}),
            'submitter': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'treasurer_kerberos': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'treasurer_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'groups.groupstatus': {
            'Meta': {'object_name': 'GroupStatus'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'groups.officeholder': {
            'Meta': {'object_name': 'OfficeHolder'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.OfficerRole']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'groups.officerrole': {
            'Meta': {'object_name': 'OfficerRole'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'grant_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_count': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'publicly_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'require_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['groups']
