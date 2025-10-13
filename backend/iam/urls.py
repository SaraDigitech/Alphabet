from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.login, name='login'),
    path('user/profile/', views.profile, name='profile'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/token/refresh/', views.refresh_access_token, name='token_refresh'),
]
