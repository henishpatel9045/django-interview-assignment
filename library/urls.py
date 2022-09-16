from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import *

router = DefaultRouter()
router.register("category", CategoryViewSet, basename="Endpoint for category of books.")
router.register("book", BookViewSet, basename="Endpoint for books.")
router.register("return", ReturnApprovalViewSet, basename="Endpoint for return approval.")

borrow = NestedDefaultRouter(router, "book", lookup="book")
borrow.register('borrow', BorrowViewSet, basename="Endpoint for borrow books.")

urlpatterns = router.urls + borrow.urls