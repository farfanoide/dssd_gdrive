from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from oauth2client.client import OAuth2WebServerFlow

class SyncGdriveView(TemplateView):

    def get(self, request, *args, **kwargs):

        flow = OAuth2WebServerFlow(
            client_id='356000299673-r1g4pasacfa7p4v85s49kcf92aeqamh3.apps.googleusercontent.com',
            client_secret='LHT7jayNUPcxv6cWqQcuB08N',
            scope='https://www.googleapis.com/auth/calendar',
            redirect_uri='http://localhost:8000/sync_gdrive_success/'
        )

        auth_uri = flow.step1_get_authorize_url()

        return HttpResponseRedirect(auth_uri)



class SyncGdriveSuccessView(View):
    pass

class GdriveListView(View):
    pass

class GdriveShareView(View):
    pass

class GdriveCreateView(View):
    pass
