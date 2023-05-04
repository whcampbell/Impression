from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/<slug:username>', views.profile, name="profile"),
    path('messages/<slug:username>', views.messages, name="messages"),
    path('message/<slug:username>/<int:id>', views.MessageView.as_view(), name="message_detail"),
]