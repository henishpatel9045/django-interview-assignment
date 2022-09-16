from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet, LoginViewSet
from rest_framework_simplejwt import views
from django.urls import path

router = DefaultRouter()
router.register("register", SignUpViewSet, basename="register")

urlpatterns = [
    path("login", views.TokenObtainPairView.as_view(), name="jwt-create"),
    path("refresh", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path("authenticate", views.TokenVerifyView.as_view(), name="jwt-verify"),
]

urlpatterns += router.urls
