from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_view, name='input_view'),
    path('optimize/', views.optimize_distribution, name='optimize'),  # <-- Make sure this line is there
    path('download_csv/', views.download_csv, name='download_csv'),
]
