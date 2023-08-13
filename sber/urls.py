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
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Сбер Афиша API')

urlpatterns = [
    # Swagger
    url(r'^$', schema_view),
    
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

    # Routes
    path('api/routes/', RouteAPIListCreateView.as_view()),
    path('api/routes/<int:pk>/', RouteAPIDetailView.as_view()),
    path('api/routes/<int:pk>/tickets/buy/', RouteAPITicketGetView.as_view()),
    path('api/routes/tickets/my/', RouteAPIMyTicketsView.as_view()),

    # Users
    path('api/users/auth/', include('djoser.urls')),
    re_path(r'^api/users/auth/', include('djoser.urls.authtoken')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
