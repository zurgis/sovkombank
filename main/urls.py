from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='main'),
    path('<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='delete'),
    path('create/', views.ApplicationCreateView.as_view(), name='create'),
    path('export-csv/', views.exportCSV, name='export_csv'),
    path('export-excel/', views.exportExcel, name='export_excel'),
    path('list/', views.app, name='list')
]