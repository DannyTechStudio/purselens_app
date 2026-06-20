from django.urls import path
from . import views

app_name = "activity"

urlpatterns = [
    path("", views.UserActivityLogListView.as_view(),   name="my-logs"),
    path("<uuid:pk>/", views.UserActivityLogDetailView.as_view(), name="my-log-detail"),
    path("admin/", views.AdminActivityLogListView.as_view(),  name="admin-logs"),
]