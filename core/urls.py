from django.urls import path, include
from .views import *


app_name = 'core'

urlpatterns = [
    path('', ProjectHandler.as_view(), name='index'),
    path('projects/', ProjectHandler.as_view(), name='projects'),
    path('select-avatars/<slug>/', SelectAvatars.as_view(), name='avatars'),
    path('select-animation/<slug>/', SelectDriver.as_view(), name='driver'),
    path('add-text/<slug>/', AddText.as_view(), name='add-text'),
    path('final-video/<slug>/', FinalVideo.as_view(), name='final-video'),
]
