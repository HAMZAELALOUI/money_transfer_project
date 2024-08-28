from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from transactions.views import TransactionViewSet
from users.views import UserViewSet
from wallets.views import WalletViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"wallets", WalletViewSet)
router.register(r"transactions", TransactionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
