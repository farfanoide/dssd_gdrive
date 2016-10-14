from __future__ import unicode_literals

from django.db import models
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
import httplib2


class GdriveRepository(object):

    def __init__(self, credentials):
        credentials = OAuth2Credentials.from_json(credentials)
        http = credentials.authorize(httplib2.Http())

        self.service = build('drive', 'v3', http=http)

    def list(self):
        return self.service.files().list(fields='files(id,name,shared)').execute().get('files')

    def create(self, name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.document',
        }
        self.service.files().create(body=file_metadata, fields='id').execute()

    def share(self, file_id, user_email):

        batch = self.service.new_batch_http_request(callback=self._callback)

        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': user_email,
        }

        batch.add(self.service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ))
        batch.execute()

    def unshare(self, file_id):
        batch = self.service.new_batch_http_request()

        permissions = self.service.permissions().list(fileId=file_id).execute()

        for permission in permissions.get('permissions'):
            if permission['role'] != 'owner':
                batch.add(self.service.permissions().delete(
                    fileId=file_id,
                    permissionId=permission['id'],
                    fields='id',
                ))

        batch.execute()

    def _callback(self, request_id, response, exception):
        if exception:
            # Handle error
            print exception
        else:
            print "Permission Id: %s" % response.get('id')

