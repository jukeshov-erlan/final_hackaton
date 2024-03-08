from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Cinema_kg',
        default_version='v1',
        description='online cinema ',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ersik.j10@gmail.com"),
        license=openapi.License(name="BSD License"),
   ),
   public=True,
    )



urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payments.urls')),
    path('api/v1/', include('movies.urls')),
    path('api/v1/account/', include('account.urls')),
    path('docs/', schema_view.with_ui('swagger'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)