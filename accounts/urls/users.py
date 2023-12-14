from django.urls import path, include
from accounts.views.drf_user_view import UserView
from accounts.views.dj_user_view import DjUserView

app_name = 'users'
urlpatterns = [
    path('', UserView.as_view(), name='users'),
    path('dj-class/', DjUserView.as_view(), name='dj-class'),
]