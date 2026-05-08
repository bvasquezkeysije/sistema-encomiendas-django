from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from envios.api_views import ClienteListAPIView, RutaListAPIView
from envios.viewsets import EncomiendaViewSet

router = DefaultRouter()
router.register("encomiendas", EncomiendaViewSet, basename="encomienda")

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="token_obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(permission_classes=[AllowAny]), name="token_refresh"),
    path("schema/", SpectacularAPIView.as_view(permission_classes=[AllowAny]), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema", permission_classes=[AllowAny]), name="swagger"),
    path("clientes/", ClienteListAPIView.as_view(), name="api_clientes"),
    path("rutas/", RutaListAPIView.as_view(), name="api_rutas"),
    path("", include(router.urls)),
]
