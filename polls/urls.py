from django.urls import path

from . import views

urlpatterns = [
    path("", views.help.as_view(), name="index"),
    path("prow", views.prowadzacy.as_view(), name="prowadzacy"),
    path("actuality", views.actuality_stud.as_view(), name="aktualizacja"),
    path("days", views.days.as_view(), name="days"),
    path("plan/stud",views.plan_stud.as_view(), name="plan"),
    path("grp",views.group_name.as_view(), name="plan"),
    path("plan/prow",views.plan_prow.as_view(), name="plan"),
    path("plan/stud/js",views.plan_stud_karwo.as_view(), name="plan"),
    path("plan/prow/js",views.plan_prow_karwo.as_view(), name="plan"),

]