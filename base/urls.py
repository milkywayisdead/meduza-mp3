from django.urls import path
from base import views

urlpatterns = [
    path('', views.index, name='index'),
    path('record/<int:record_id>/', views.record, name='record'),
    path('api/v1/records/', views.get_records, name='get_records'),
    path('api/v1/records/<int:record_id>', views.get_record, name='get_record'),
]