from django.urls import path
from .import views

urlpatterns = [
    path("<int:id>", views.index, name = "index"),
    path("create/", views.create, name = "create"),
    path("", views.home, name = "home"),
    path("Systeempomp/<int:id>/",views.systeempomp_view, name="SysteemPomp"),
    path("Doseerpomp/<int:id>/",views.doseerpomp_view, name="DoseerPomp"),
    path("Literteller/<int:id>/",views.literteller_view, name="Literteller"),
    path("Waterfilter/<int:id>/",views.waterfilter_view, name="Waterfilter"),
    path("Doseerstraat/<int:id>/",views.doseerstraat_view, name="Doseerstraat"),
    path("Meetstraat/<int:id>/",views.meetstraat_view, name="Meetstraat"),
    path("Stop/", views.stop_view, name="Stop"),
    path("Start/", views.startopcua_view, name="Start"),
]