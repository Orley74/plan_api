from django.urls import path

from . import views

urlpatterns = [
    path("groups", views.get_group_name, name="index"),
    path("actuality_plan", views.check_actuality_plan, name="aktualizacja"),
    path("days", views.get_days, name="days"),
    path("plan",views.get_plan, name="index")
]