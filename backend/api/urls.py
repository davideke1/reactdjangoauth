from django.urls import path
from .views import UserProfileCreateView, HomeView, LogoutView

urlpatterns = [
    # path('register/', UserRegistrationView.as_view(), name='register'),
    path('register/', UserProfileCreateView.as_view(), name='register'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name ='logout')
]
