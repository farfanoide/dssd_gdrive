from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from django.http import HttpResponseRedirect
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from django.conf.urls import url
from django.core.urlresolvers import reverse, reverse_lazy
from .models import GdriveRepository
from .forms import GdriveShareForm

from apiclient.discovery import build
import httplib2

import json

flow = OAuth2WebServerFlow(
    client_id='356000299673-r1g4pasacfa7p4v85s49kcf92aeqamh3.apps.googleusercontent.com',
    client_secret='LHT7jayNUPcxv6cWqQcuB08N',
    scope='https://www.googleapis.com/auth/drive',
    redirect_uri='http://localhost:8000/sync_gdrive_success/'
)


class HomeView(TemplateView):

    template_name = 'home.html'


class SyncGdriveView(TemplateView):

    def get(self, request, *args, **kwargs):

        auth_uri = flow.step1_get_authorize_url()

        return HttpResponseRedirect(auth_uri)


class SyncGdriveSuccessView(View):

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)

        if not code:
            return False

        credentials = flow.step2_exchange(code)
        request.session['credentials'] = credentials.to_json()

        return HttpResponseRedirect(reverse('list'))


class GdriveListView(TemplateView):

    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super(GdriveListView, self).get_context_data(**kwargs)
        context['items'] = GdriveRepository(self.request.session['credentials']).list()
        return context


class GdriveShareView(FormView):
    template_name = 'share.html'
    success_url = reverse_lazy('list')
    form_class = GdriveShareForm


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user_email = form.cleaned_data.get('user_email')
            file_id = kwargs.get('file_id')
            GdriveRepository(self.request.session['credentials']).share(file_id, user_email)


class GdriveCreateView(View):

    def post(self, request, *args, **kwargs):
        name = self.request.POST['new_file']
        GdriveRepository(self.request.session['credentials']).create(name)

        return HttpResponseRedirect(reverse('list'))
