from django.urls import path
from dashboard import views

urlpatterns = [

    path('dashboard/', views.index, name='dashboard-index'),

    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:key>', views.staff_detail, name='dashboard-staff-detail'),

    path('product/', views.product, name='dashboard-product'),
    path('product/delete/<int:key>/', views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:key>/', views.product_update, name='dashboard-product-update'),

    path('order/', views.order, name='dashboard-order'),
    path('order/order-dispatch/<int:key>', views.dispatch, name='dashboard-order-dispatch'),
    path('order/order-delete/<int:key>', views.delete_order, name='dashboard-order-delete'),
    
    path('flash-messages/', views.flash_messages, name='dashboard-flash-messages'),
    path('flash-messages/delete/<int:key>/<int:check>', views.flash_messages_delete, name='dashboard-flash-messages-delete'),
    

]