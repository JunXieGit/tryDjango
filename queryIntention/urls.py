from django.urls import path

from queryIntention import views

app_name = 'queryIntention'

urlpatterns = [
    path('', views.demo, name='query_intention_demo'),
    path('make_member/', views.make_member, name='make_member'),
    path('memberId_checker', views.memberId_checker, name='memberId_checker'),

]