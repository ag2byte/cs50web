from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('transactions/<str:rec_type>', views.transactions, name='transactions'),
    path('index',views.index,name='index'),
    path('logout',views.logout_view,name='logout'),
    path('newentry',views.newentry,name='newentry'),

]
