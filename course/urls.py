from django.conf.urls import patterns, include, url
from course import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fkpro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test/', views.test, name='test'),
    url(r'^login/', views.login, name='login'),
    url(r'^(?P<student>\d+)/(?P<day>\d+)/(?P<num>\d+)/',
        views.getCourse, name='get_course'),
)
