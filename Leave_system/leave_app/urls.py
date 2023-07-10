from django.urls import path
from leave_app import views

urlpatterns = [


    # path('logout', views.logout),
    
    
    path('', views.home),
    path('info', views.info),
    path('login',views.login),
    path('hr', views.hr),
    path('HRleader/', views.HRleader),
    path('leader/', views.leader),
    path('createForm/', views.createForm),
    path('addForm/', views.addForm),
    path('result/', views.result),
    path('logout', views.logout),
    path('formleave',views.formleave),
    path('status',views.status),
    path('approve',views.approve),
    path('success/<person_id>',views.success),
    path('unsuccess/<person_id>',views.unsuccess),
]
