from django.urls import path

from webapp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('project_index/', views.ProjectView.as_view(), name='project_index'),
    path('project/<int:pk>/', views.ProjectDetail.as_view(), name='project_view'),
    path('project/add/', views.ProjectAdd.as_view(), name='project_add'),
    path('tracker/<int:pk>/', views.TrackerDetail.as_view(), name='tracker_view'),
    path('add_view/', views.TrackerAdd.as_view(), name='add_view'),
    path('tracker/<int:pk>/update', views.TrackerUpdateView.as_view(), name='tracker_update'),
    path('tracker/<int:pk>/delete/', views.DeleteTrackerView.as_view(), name='tracker_delete'),
    path('tracker/<int:pk>/confirm_delete/', views.DeleteTrackerView.as_view(), name='confirm_delete')
]