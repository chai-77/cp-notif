from rest_framework.routers import DefaultRouter
from contests.views import ContestViewSet



router = DefaultRouter()
router.register(r"contests", ContestViewSet)

urlpatterns = router.urls