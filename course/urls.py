from django.conf.urls import patterns, include, url
from course import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fkpro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test/', views.test, name='test'),
    url(r'^login/', views.login, name='login'),
    url(r'^alarm/', views.alarm, name='alarm'),
    url(r'^gcm/(?P<student>\d+)', views.gcm, name='gcm'),
    url(r'^(?P<student>\d+)/$', views.getCourse, name='get_course'),
    url(r'^(?P<student>\d+)/now/$', views.getNow, name='get_now'),
    url(r'^(?P<student>\d+)/(?P<day>\d+)/$',
        views.getCourse, name='get_course'),
    url(r'^(?P<student>\d+)/(?P<day>\d+)/(?P<num>\d+)/',
        views.getCourse, name='get_course'),
)
