from django.urls import path

from . import views

urlpatterns = [
    path("", views.help.as_view(), name="index"),
    path("prowadzacy", views.prowadzacy.as_view(), name="prowadzacy"),
    path("actuality/stud", views.actuality_stud.as_view(), name="aktualizacja"),
    path("days", views.days.as_view(), name="days"),
    path("plan/stud",views.plan_stud.as_view(), name="plan"),
    path("grp",views.group_name.as_view(), name="plan"),
    path("plan/prow",views.plan_prow.as_view(), name="plan"),

]