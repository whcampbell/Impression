from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('edit-profile/<slug:pk>', views.UserUpdateView.as_view(), name="update"),
    path('profile/<slug:username>', views.profile, name="profile"),
    path('gallery/', views.gallery, name="gallery"),
    path('messages/', views.messages, name="messages"),
    path('compose_message', views.message_create, name='compose_message'),
    path('message/<int:id>', views.message_detail, name="message_detail"),
    path('send-friends/<slug:receiver>', views.send_friends, name="send_friends"),
    path('make-friends/<slug:sender>', views.make_friends, name="make_friends"),
    path('manage-friends/', views.manage_friends, name="manage_friends"),
    path('remove-friend/<slug:username>', views.remove_friend, name="remove_friend"),
    path('write-post', views.WritePostView.as_view(), name="write_post"),
    path('read-post/<int:id>', views.read_post, name="read_post"),
    path('delete-post/<int:id>', views.delete_post, name="delete_post"),
]