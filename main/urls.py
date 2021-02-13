from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='index'),
    path('<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='delete'),
    path('create/', views.ApplicationCreateView.as_view(), name='create'),
    path('export-csv/', views.exportCSV, name='export_csv'),
    path('export-excel/', views.exportExcel, name='export_excel'),
    path('count-application/', views.count_application, name='count_application'),
    path('last-application/', views.last_application, name='last_application'),
    path('another-product/', views.another_product, name='another_product'),
]