from django.test import TestCase, RequestFactory
from .models import CustomUser, Message
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


# Test actions with the 'Message' model
class MessageTestCase(TestCase) :
    def setUp(self) :
        self.user_one = create_user("Tets", "tets@gmail.com")
        self.user_two = create_user("Test2", "test2@gmail.com")

    def test_create_message(self) :
        Message.objects.create(
            title = "Test Message",
            body = "this is a test",
            sender = self.user_one,
            receiver = self.user_two,
        ).save()

        self.assertEqual(self.user_one.sent_messages.all().count(), 1)
        self.assertEqual(self.user_two.received_messages.all().count(), 1)


# Test the views which add friend-to-friend relationships
class FriendsTestCase(TestCase) :
    def setUp(self) :
        self.one = create_user("friend_1", "one@gmail.com")
        self.two = create_user("friend_2", "two@gmail.com")
        self.factory = RequestFactory()

    def test_send_friends(self) :
        request = self.factory.get("/users/send-friends/friend_2")
        request.user = self.one
        response = views.send_friends(request, "friend_2")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.two.received_messages.all().count(), 1)

    def test_accept_friends(self) :
        request = self.factory.get("/users/make-friends/friend_1")
        request.user = self.two
        response = views.make_friends(request, "friend_1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.one.friends.count(), 1)

        # test adding a duplicate friend from the other way around
        # (should not break or change anything)
        request.user = self.one
        views.make_friends(request, "friend_2")
        self.assertEqual(self.two.friends.count(), 1)

# Create your tests here.
