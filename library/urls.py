from rest_framework_nested.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("category", CategoryViewSet, basename="Endpoint for category of books.")

urlpatterns = router.urls