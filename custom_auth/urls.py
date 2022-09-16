from rest_framework_nested.routers import DefaultRouter
from .views import SignUpViewSet, LibrarienViewSet, MemberViewSet
from rest_framework_simplejwt import views
from django.urls import path

router = DefaultRouter()
router.register("register", SignUpViewSet, basename="register")
router.register("librarien", LibrarienViewSet, basename="Endpoint for librarien.")
router.register("member", MemberViewSet, basename="Endpoint for member.")

urlpatterns = [
    path("login", views.TokenObtainPairView.as_view(), name="Generate JWT access token using username and password."),
    path("refresh", views.TokenRefreshView.as_view(), name="Generate JWT access token using refresh token."),
    path("authenticate", views.TokenVerifyView.as_view(), name="Verigy your access token."),
]

urlpatterns += router.urls
