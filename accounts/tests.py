from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class AccountViewTests(TestCase):
    def test_signup_shows_success_message_after_redirect(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newstudent",
                "email": "student@example.com",
                "first_name": "New",
                "last_name": "Student",
                "course": "Biology",
                "password1": "Secure-test-password-593!",
                "password2": "Secure-test-password-593!",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Your account has been created successfully.")
        self.assertTrue(CustomUser.objects.filter(username="newstudent").exists())

    def test_profile_update_edits_only_logged_in_users_profile(self):
        user = CustomUser.objects.create_user(
            username="student",
            password="Secure-test-password-593!",
            role=CustomUser.Role.STUDENT,
            course="Biology",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("profile"),
            {
                "username": "updatedstudent",
                "email": "updated@example.com",
                "first_name": "Updated",
                "last_name": "Student",
                "course": "Chemistry",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertContains(response, "Your profile has been updated.")
        user.refresh_from_db()
        self.assertEqual(user.username, "updatedstudent")
        self.assertEqual(user.email, "updated@example.com")
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.last_name, "Student")
        self.assertEqual(user.course, "Chemistry")
        self.assertEqual(user.role, CustomUser.Role.STUDENT)

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )
