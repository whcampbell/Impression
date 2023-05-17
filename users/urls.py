from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/<slug:username>', views.profile, name="profile"),
    path('messages/', views.messages, name="messages"),
    path('compose_message', views.message_create, name='compose_message'),
    path('message/<int:id>', views.message_detail, name="message_detail"),
    path('send-friends/<slug:receiver>', views.send_friends, name="send_friends"),
    path('make-friends/<slug:sender>', views.make_friends, name="make_friends"),
]