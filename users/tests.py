from django.test import TestCase
from .models import CustomUser

class UserTestCase(TestCase) :
    def setUp(self) :
        user = "TEST"
        email = "test@gmail.com"
        since = "2000-09-20"
        testuser = CustomUser.objects.create(
            username=user, 
            email=email,
            artist_since=since,
            )
        testuser.set_password("thisisatest00")
        testuser.save()
    
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



# Create your tests here.
