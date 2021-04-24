from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Assets
from .serializers import UserSerializer, AssetsSerializer, UserValueSerializer, ApplicationRedemptionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserValueSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)


class AssetsViewSet(viewsets.ModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_name='operation')
    def operation(self, request, pk=None):
        get_object_or_404(self.queryset, pk=pk)
        request.data.update({"user": request.user.id, "ip": self._get_ip(request)})
        serializer = ApplicationRedemptionSerializer(data=request.data)
        if serializer.is_valid():
            x = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        else:
            return request.META.get('REMOTE_ADDR')