from django.urls import path, include
from .views import CustomLoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("",include(router.urls)),
    path("login/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),  # Adicionamos o refresh token
]
