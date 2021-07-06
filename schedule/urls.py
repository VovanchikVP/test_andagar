from schedule import views
from django.urls import path

urlpatterns = [
    # PAGE
    path('', views.analytic_page),

    # API
    path('api_v1/get_file/', views.pars_file_xml),

    ]
