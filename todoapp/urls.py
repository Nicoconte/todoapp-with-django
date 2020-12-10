from django.contrib import admin
from django.urls import path, include
from users import urls
from tasks import urls
from public import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("public.urls")),
    path('user/', include("users.urls"))
]
