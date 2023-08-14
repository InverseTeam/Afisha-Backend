"""HelloDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from sber.settings import MEDIA_ROOT, MEDIA_URL
from users.views import *
from events.views import *
from routes.views import *
from rest_framework import routers
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title='Сбер афиша API',
      default_version='v1',
      description='Платформа для планирования мероприятий и составления маршрутов по туристическим местам в Екатерибурге',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='belogurov.ivan@list.ru'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Events
    path('api/events/', EventAPIListCreate.as_view()),
    path('api/events/filter/', EventAPIFilterListView.as_view()),
    path('api/events/<int:pk>/', EventAPIDetailView.as_view()),
    path('api/events/images/create/', EventImageAPICreateView.as_view()),
    path('api/events/<int:pk>/comments/add/', CommentAPICreateView.as_view()),
    path('api/events/platforms/', PlatformAPIListView.as_view()),
    path('api/events/platforms/<int:pk>/', PlatformAPIDetailView.as_view()),
    path('api/events/categories/', CategoryAPIListView.as_view()),
    path('api/events/categories/<int:pk>/', EventAPICategoryListView.as_view()),
    path('api/events/<int:pk>/tickets/create/', TicketAPICreateView.as_view()),
    path('api/events/tickets/my/', TicketAPIMyListView.as_view()),
    path('api/events/generate/', generate_events),
    path('api/events/not_published/list/', EventAPINotPublishedView.as_view()),

    # Routes
    path('api/routes/', RouteAPIListCreateView.as_view()),
    path('api/routes/<int:pk>/', RouteAPIDetailView.as_view()),
    path('api/routes/<int:pk>/tickets/create/', RouteAPITicketGetView.as_view()),
    path('api/routes/tickets/my/', RouteAPIMyTicketsView.as_view()),

    # Users
    path('api/users/auth/', include('djoser.urls')),
    re_path(r'^api/users/auth/', include('djoser.urls.authtoken')),

    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
