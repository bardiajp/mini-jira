from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'auth', AuthViewSet)

urlpatterns = router.urls + [
    path('auth/login/', TokenObtainPairView.as_view()),
]
