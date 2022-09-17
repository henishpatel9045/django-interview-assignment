<<<<<<< HEAD
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import MeViewSet, SignUpViewSet, LibrarienViewSet, MemberViewSet
from rest_framework_simplejwt import views
from django.urls import path
from library.views import BorrowByUserViewSet
=======
from rest_framework_nested.routers import DefaultRouter
from .views import SignUpViewSet, LibrarienViewSet, MemberViewSet
from rest_framework_simplejwt import views
from django.urls import path
>>>>>>> 22cb0a06791def321334ad8136481e698ae7b07f

router = DefaultRouter()
router.register("register", SignUpViewSet, basename="register")
router.register("librarien", LibrarienViewSet, basename="Endpoint for librarien.")
router.register("member", MemberViewSet, basename="Endpoint for member.")
<<<<<<< HEAD
router.register("me", MeViewSet, basename="Endpoint for me.")

me_router = NestedDefaultRouter(router, "me", lookup="me")
me_router.register("borrowed", BorrowByUserViewSet, basename="Endpoint for me.")  

=======

>>>>>>> 22cb0a06791def321334ad8136481e698ae7b07f
urlpatterns = [
    path("login", views.TokenObtainPairView.as_view(), name="Generate JWT access token using username and password."),
    path("refresh", views.TokenRefreshView.as_view(), name="Generate JWT access token using refresh token."),
    path("authenticate", views.TokenVerifyView.as_view(), name="Verigy your access token."),
]

<<<<<<< HEAD
urlpatterns += router.urls + me_router.urls
=======
urlpatterns += router.urls
>>>>>>> 22cb0a06791def321334ad8136481e698ae7b07f
