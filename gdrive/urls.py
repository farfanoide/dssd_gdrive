from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^sync_gdrive/$', SyncGdriveView.as_view()),
    url(r'^sync_gdrive_success/$', SyncGdriveSuccessView.as_view()),
    url(r'^list/$', GdriveListView.as_view()),
    url(r'^share/$', GdriveShareView.as_view()),
    url(r'^create/$', GdriveCreateView.as_view()),
]

