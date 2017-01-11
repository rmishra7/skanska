
from django.conf.urls import url
from projects import apis

urlpatterns = [
    url(r'^$', apis.ProjectApi.as_view(), name="api_projects_list")
]
