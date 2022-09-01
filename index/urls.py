from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("base/",views.base,name="base"),
    path("result",views.result,name="result"),
    path("test",views.test,name="test"),
]