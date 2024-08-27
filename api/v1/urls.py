from django.urls import path, include

urlpatterns = [
    path("users/", include("users.urls")),
    path("transactions/", include("transactions.urls")),
    path("agents/", include("agents.urls")),
    path("wallets/", include("wallets.urls")),
]
