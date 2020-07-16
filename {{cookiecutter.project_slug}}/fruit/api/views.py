from fruit.api.serializers import FruitDefaultSerializer, FruitDetailSerializer
from fruit.models import Fruit
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class FruitViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = Fruit.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FruitDetailSerializer
        else:
            return FruitDefaultSerializer
