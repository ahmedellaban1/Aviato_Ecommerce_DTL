from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar



urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls'),),
    path('accounts/', include('accounts.urls', namespace="accounts-customized-url")),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('products.urls', namespace='products-main-url')),
    path('orderhub/', include('orderhub.urls', namespace='orderhub-main-url'))

]



# Debug Toolbar only in DEBUG mode
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
