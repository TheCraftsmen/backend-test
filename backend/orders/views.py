import logging

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Menu, Order
from .serializers import MenuSerializer, OrderSerializer


class MenuAdminView(APIView):
    """APIView for admin user.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Menu.objects.all()

    def get(self, request):
        """
        Return  all menus.
        """
        menu = self.get_queryset()
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create menus, only for admin users
        """
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailAdminView(APIView):
    """APIView for admin user.

    * Menu detail endpoint for admin user.
    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self, pk):
        return get_object_or_404(Menu, id=pk)

    def get(self, request, pk):
        """Return menu details."""
        menu = self.get_queryset(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Delete menu, (require pk)."""
        menu = self.get_queryset(pk)
        menu.delete()
        return Response({}, status=status.HTTP_200_OK)


class OrderAdminView(APIView):
    """APIView for admin user.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """Return all users orders"""
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuView(APIView):
    """APIView for all user.

    * Requires token authentication.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.all()

    def get(self, request):
        """
        Return  all menus.
        """
        menu = self.get_queryset()
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuDetailView(APIView):
    """APIView for all user.

    * Menu detail endpoint for user.
    """

    def get_queryset(self, pk):
        return get_object_or_404(Menu, id=pk)

    def get(self, request, pk):
        """Return menu details."""
        menu = self.get_queryset(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    """APIView for all users.

    * Return orders, actions: get, post.
    * Requires token authentication.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get(self, request):
        """Return only user orders."""
        order = self.get_queryset()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create user orders."""
        serializer = OrderSerializer(
            data=request.data, context={'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """APIView for all users.

    * Return order detail, actions: get, patch, delete
    * Requires token authentication.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self, pk):
        order = Order.objects.filter(user=self.request.user)
        return get_object_or_404(order, id=pk)

    def get(self, request, pk):
        """Return order detail for user order only. (require pk)."""
        order = self.get_queryset(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Permit modify a created order. (require pk)."""
        order = self.get_queryset(pk)
        serializer = OrderSerializer(order, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Permit delete a created order. (require pk)."""
        order = self.get_queryset(pk)
        order.delete()
        return Response({}, status=status.HTTP_200_OK)
