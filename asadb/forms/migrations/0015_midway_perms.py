# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

app_label = 'forms'
models = [
    'midway',
    'midwayassignment',
]
verbs = [
    'add',
    'change',
    'delete',
]

class Migration(DataMigration):

    def build_perms(self, orm, models, verbs):
        ret = []
        for model in models:
            ct = orm['contenttypes.ContentType'].objects.get(model=model, app_label=app_label, )
            ret.extend([(ct, "%s_%s" % (verb, model, )) for verb in verbs])
        return ret

    def modify_perms(self, orm, perms_mod):
        "Write your forwards methods here."
        group_obj = orm['auth.Group'].objects.get(name='asa-ebm')
        pairs = self.build_perms(orm, models, verbs)
        for ct, codename in pairs:
            perms_mod(group_obj.permissions, orm['auth.permission'].objects.get(
                content_type=ct,
                codename=codename,
            ))

    def forwards(self, orm):
        "Write your forwards methods here."

        # See https://groups.google.com/forum/?fromgroups=#!topic/south-users/ZmmUyrrRoYU or groups:0006_add_group_perms
        db.send_pending_create_signals()

        self.modify_perms(orm, lambda perms, perm: perms.add(perm))


    def backwards(self, orm):
        "Write your backwards methods here."
        self.modify_perms(orm, lambda perms, perm: perms.remove(perm))


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 24, 0, 8, 12, 980849)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 24, 0, 8, 12, 980761)'}),
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
        'forms.fysm': {
            'Meta': {'object_name': 'FYSM'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['forms.FYSMCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_preview': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms.PagePreview']", 'null': 'True'}),
            'join_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slide': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'forms.fysmcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'FYSMCategory'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'forms.fysmview': {
            'Meta': {'object_name': 'FYSMView'},
            'fysm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms.FYSM']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'referer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'source_user': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'forms.groupconfirmationcycle': {
            'Meta': {'object_name': 'GroupConfirmationCycle'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deadlines': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'forms.groupmembershipupdate': {
            'Meta': {'object_name': 'GroupMembershipUpdate'},
            'cycle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms.GroupConfirmationCycle']"}),
            'email_preface': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'group_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_definition': ('django.db.models.fields.TextField', [], {}),
            'membership_list': ('django.db.models.fields.TextField', [], {}),
            'no_discrimination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_hazing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_alum': ('django.db.models.fields.IntegerField', [], {}),
            'num_grads': ('django.db.models.fields.IntegerField', [], {}),
            'num_other': ('django.db.models.fields.IntegerField', [], {}),
            'num_other_affiliate': ('django.db.models.fields.IntegerField', [], {}),
            'num_undergrads': ('django.db.models.fields.IntegerField', [], {}),
            'officer_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'updater_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updater_title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'forms.midway': {
            'Meta': {'object_name': 'Midway'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'table_map': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'forms.midwayassignment': {
            'Meta': {'object_name': 'MidwayAssignment'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'midway': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms.Midway']"})
        },
        'forms.pagepreview': {
            'Meta': {'object_name': 'PagePreview'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'forms.personmembershipupdate': {
            'Meta': {'object_name': 'PersonMembershipUpdate'},
            'cycle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forms.GroupConfirmationCycle']"}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['groups.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'valid': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'groups.activitycategory': {
            'Meta': {'object_name': 'ActivityCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'groups.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'blank': 'True'}),
            'activity_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.ActivityCategory']", 'null': 'True', 'blank': 'True'}),
            'advisor_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'athena_locker': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'constitution_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'funding_account_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.GroupClass']"}),
            'group_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'group_funding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.GroupFunding']", 'null': 'True', 'blank': 'True'}),
            'group_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.GroupStatus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_account_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_times': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'num_community': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_grads': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_other': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_undergrads': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'officer_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'recognition_date': ('django.db.models.fields.DateTimeField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updater': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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
        'groups.groupstatus': {
            'Meta': {'object_name': 'GroupStatus'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['forms', 'auth', 'forms']
