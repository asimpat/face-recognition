from django.urls import path
from .views import SignupView, LoginView, FaceEnrollView, FaceVerifyView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('faces/enroll/', FaceEnrollView.as_view(), name='face-enroll'),
    path('faces/verify/', FaceVerifyView.as_view(), name='face-verify'),
]
