from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('jobs/', views.jobs, name='jobs'),
    url('awards/', views.awards, name='awards'),
    url(r'^job/(?P<job_id>[0-9]+)/$', views.job_detail, name='job_detail'),
    url(r'^award/(?P<award_id>[0-9]+)/$', views.award_detail, name='award_detail'),
    ]
