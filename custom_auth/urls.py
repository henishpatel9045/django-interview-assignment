from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet

router = DefaultRouter()
router.register("register", SignUpViewSet, basename="register")

urlpatterns = router.urls
