from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^sync_gdrive/$', SyncGdriveView.as_view(), name='sync'),
    url(r'^sync_gdrive_success/$', SyncGdriveSuccessView.as_view()),
    url(r'^list/$', GdriveListView.as_view(), name='list'),
    url(r'^(?P<file_id>.+)/share/$', GdriveShareView.as_view(), name='share'),
    url(r'^(?P<file_id>.+)/unshare/$', GdriveUnshareView.as_view(), name='unshare'),
    url(r'^create/$', GdriveCreateView.as_view(), name='create'),
]

