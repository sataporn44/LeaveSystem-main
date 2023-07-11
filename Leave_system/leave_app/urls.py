from django.urls import path
from leave_app import views

urlpatterns = [


    # path('logout', views.logout),
    
    
    path('', views.home),
    path('info', views.info, name='info'),
    path('login',views.login),
    path('createForm/', views.createForm),
    path('addForm/', views.addForm),
    path('result/', views.result),
    path('logout', views.logout),
    path('formleave',views.formleave),
    path('edit/<person_id>/',views.edit, name='edit'), ##(ชื่อpath/<ชื่อพารามิเตอร์>,กระบวนการทำงาน)
    path('delete/<person_id>/',views.delete),
    path('status/',views.status),
    path('approve',views.approve),
    path('success/<person_id>',views.success),
    path('unsuccess/<person_id>',views.unsuccess),
]
