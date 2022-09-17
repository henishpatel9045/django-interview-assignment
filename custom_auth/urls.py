from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import MeViewSet, SignUpViewSet, LibrarienViewSet, MemberViewSet
from rest_framework_simplejwt import views
from django.urls import path
from library.views import BorrowByUserViewSet

router = DefaultRouter()
router.register("register", SignUpViewSet, basename="register")
router.register("librarien", LibrarienViewSet, basename="Endpoint for librarien.")
router.register("member", MemberViewSet, basename="Endpoint for member.")
router.register("me", MeViewSet, basename="Endpoint for me.")

me_router = NestedDefaultRouter(router, "me", lookup="me")
me_router.register("borrowed", BorrowByUserViewSet, basename="Endpoint for me.")  

urlpatterns = [
    path("login", views.TokenObtainPairView.as_view(), name="Generate JWT access token using username and password."),
    path("refresh", views.TokenRefreshView.as_view(), name="Generate JWT access token using refresh token."),
    path("authenticate", views.TokenVerifyView.as_view(), name="Verigy your access token."),
]

urlpatterns += router.urls + me_router.urls
