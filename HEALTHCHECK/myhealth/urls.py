from django.urls import path
from . import views

urlpatterns = [
    path('list', views.listfunc, name='list'),
    path('create', views.ScrapeCreate.as_view(), name='create'),
    path('update/<int:pk>', views.DiaryUpdate.as_view(), name='update'),
    path('analysis', views.analysis, name='analysis'),
    path('signup', views.signupfunc, name='signup'),
    path('login', views.loginfunc, name='login'),
    path('logout', views.logoutfunc, name='logout'),
    path('graph', views.graph, name='graph'),
]