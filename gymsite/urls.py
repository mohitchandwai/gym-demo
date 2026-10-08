from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings
admin.site.site_header = "Gym Admin"
urlpatterns = [path("admin/", admin.site.urls), path("", include("core.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})]
