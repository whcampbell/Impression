from django.test import TestCase, RequestFactory, Client
from .models import CustomUser, Message, BlogPost
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from . import views

# Helpers
def create_user(username, email) :
    testuser = CustomUser.objects.create(
        username=username, 
        email=email,
        artist_since="2000-03-20",
        )
    testuser.set_password("thisisatest00")
    testuser.save()
    return testuser

def create_msg(user1, user2, title) :
    return Message.objects.create(
        sender = user1,
        receiver = user2,
        title = title,
        body = "hello there",
    )


# Tests

# Test actions with the 'CustomUser' model
class UserTestCase(TestCase) :
    def setUp(self) :
        self.user = create_user("TEST", "test@gmail.com")
    
    def test_user_created(self) :
        self.assertEqual(self.user.username, "TEST")

    def test_user_authentication(self) :
        self.assertTrue(self.user.is_authenticated)

    def test_check_password(self) :
        self.assertTrue(self.user.check_password("thisisatest00"))


# Test actions with the 'Message' model and views
class MessageTestCase(TestCase) :
    def setUp(self) :
        self.user_one = create_user("Tets", "tets@gmail.com")
        self.user_two = create_user("Test2", "test2@gmail.com")
        self.client = Client()
        self.client.login(username='Test2', password='thisisatest00')

    def test_create_message(self) :
        Message.objects.create(
            title = "Test Message",
            body = "this is a test",
            sender = self.user_one,
            receiver = self.user_two,
        ).save()

        self.assertEqual(self.user_one.sent_messages.all().count(), 1)
        self.assertEqual(self.user_two.received_messages.all().count(), 1)

    def test_show_most_recent_only(self) :
        create_msg(self.user_one, self.user_two, "first")
        create_msg(self.user_one, self.user_two, "second")

        response = self.client.get("/users/messages/")
        messages = response.context['messages']
        self.assertEqual(len(messages), 1)
        self.assertEqual(response.context['messages'][0].title, "second")

    def test_cannot_see_others_mail(self) :
        msg = create_msg(self.user_one, self.user_two, "secret stuff")
        url = '/users/message/' + str(msg.pk)
        create_user("black_hat", "badguy@gmail.com")
        self.client.logout()
        self.client.login(username="black_hat", password="thisisatest00")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


# Test the views which add friend-to-friend relationships
class FriendsTestCase(TestCase) :
    def setUp(self) :
        self.one = create_user("friend_1", "one@gmail.com")
        self.two = create_user("friend_2", "two@gmail.com")
        self.factory = RequestFactory()
        self.client = Client()

    def test_send_friends(self) :
        request = self.factory.get("/users/send-friends/friend_2")
        request.user = self.one
        response = views.send_friends(request, "friend_2")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.two.received_messages.all().count(), 1)

    def test_make_friends(self) :
        try :
            list(Message.objects.get(sender=self.one, receiver=self.two))
        except ObjectDoesNotExist :
            request = self.factory.get("/users/send-friends/friend_2")
            request.user = self.one
            views.send_friends(request, "friend_2")  

        request = self.factory.get("/users/make-friends/friend_1")
        request.user = self.two
        response = views.make_friends(request, "friend_1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.one.friends.count(), 1)

    def test_make_friends_non_consentually(self) :
        request = self.factory.get("/users/make-friends/friend_2")
        request.user = self.one
        try :
            views.make_friends(request, "friend_2")
            self.assertEqual(1, 2)
        except PermissionDenied :
            self.assertEqual(1, 1)
    
    def test_remove_friend(self) :
        self.one.friends.add(self.two)
        self.assertEqual(self.one.friends.count(), 1)

        self.client.logout()
        self.client.login(username="friend_1", password="thisisatest00")

        self.client.get('/users/remove-friend/' + self.two.username)
        self.assertEqual(self.one.friends.count(), 0)

    def test_remove_already_isnt_friend(self) :
        self.client.logout()
        create_user("black_hat", "badguy@gmail.com")
        self.client.login(username="black_hat", password="thisisatest00")

        response = self.client.get('/users/remove-friend/' + self.one.username)
        self.assertEqual(response.status_code, 302)

class BlogTestCase(TestCase) :
    def setUp(self) :
        self.user = create_user("influencer", "foot_master@onlyfans.com")
        self.post = BlogPost.objects.create(
            user=self.user, 
            title="Who let the dogs out?",
        )
        self.pk = self.post.pk
        self.client = Client()
    
    def test_no_other_posts(self) :
        url = '/users/read-post/' + str(self.pk)
        response = self.client.get(url)
        curr = response.context['curr_post']
        posts = response.context['post_list']
        self.assertEqual(curr.title, "Who let the dogs out?")
        self.assertEqual(posts.count(), 0)
    
    def test_deleting_others_posts_forbidden(self) :
        create_user("black_hat", "badguy@gmail.com")
        self.client.logout()
        self.client.login(username="black_hat", password="thisisatest00")
        url = '/users/delete-post/' + str(self.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.post.title, "Who let the dogs out?")


# Create your tests here.
