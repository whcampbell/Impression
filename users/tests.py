from django.test import TestCase
from .models import CustomUser, Message

# Helpers
def create_user(username, email) :
    testuser = CustomUser.objects.create(
        username=username, 
        email=email,
        artist_since="2000-03-20",
        )
    testuser.set_password("thisisatest00")
    testuser.save()

class UserTestCase(TestCase) :
    def setUp(self) :
        create_user("TEST", "test@gmail.com")
    
    def test_user_created(self) :
        testuser = CustomUser.objects.get(username="TEST")
        self.assertEqual(testuser.username, "TEST")

    def test_user_authentication(self) :
        testuser = CustomUser.objects.get(username="TEST")
        self.assertTrue(testuser.is_authenticated)

    def test_check_password(self) :
        testuser = CustomUser.objects.get(username="TEST")
        #testuser.set_password("thisisatest00")
        self.assertTrue(testuser.check_password("thisisatest00"))

class MessageTestCase(TestCase) :
    def setUp(self) :
        create_user("TEST", "test@gmail.com")
        create_user("Test2", "test2@gmail.com")

    def test_create_message(self) :
        testuser = CustomUser.objects.get(username="TEST")
        testuser2 = CustomUser.objects.get(username="Test2")

        Message.objects.create(
            title = "Test Message",
            body = "this is a test",
            sender = testuser,
            receiver = testuser2,
        ).save()

        self.assertTrue(testuser.sent_messages.all())
        self.assertTrue(testuser2.received_messages.all())


# Create your tests here.
