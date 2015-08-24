# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tags_app_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tagline', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'tags_app', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'tags_app_tag')


    models = {
        u'tags_app.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['tags_app']