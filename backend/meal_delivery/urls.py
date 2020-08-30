"""meal_delivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from orders import views

urlpatterns = [
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
    path('api/admin/menu', views.MenuAdminView.as_view(), name='admin_menu'),
    path('api/admin/menu/<int:pk>', views.MenuDetailAdminView.as_view(), name="admin_menu_detail"),
    path('api/admin/order', views.OrderAdminView.as_view(), name='admin_order'),
    path('api/menu', views.MenuView.as_view(), name='menu'),
    path('api/menu/<int:pk>', views.MenuDetailView.as_view(), name="menu_detail"),
    path('api/order', views.OrderView.as_view(), name="order"),
    path('api/order/<int:pk>', views.OrderDetailView.as_view(), name="order_detail")
]
