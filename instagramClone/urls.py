from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^upload/$', views.upload_image, name='upload_image'),
    url(r'^user/(?P<username>\w+)',views.edit_profile, name='edit_profile'),
    url(r'^accounts/editprofile/',views.editprofile, name='editprofile'),
    url(r'^image/(?P<image_id>\d+)', views.single_image, name='single_image'),
    url(r'^search/', views.search, name='search'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'^like/(?P<image_id>\d+)', views.like, name='like'),
    url(r'^follow/(?P<user_id>\d+)', views.follow, name='follow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

