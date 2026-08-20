from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Expense


class ExpenseApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.alice = user_model.objects.create_user(username="alice", password="pass1234")
        self.bob = user_model.objects.create_user(username="bob", password="pass1234")
        self.client.force_authenticate(user=self.alice)
        Expense.objects.create(
            owner=self.alice,
            amount="12.50",
            description="Coffee",
            category="Food",
        )
        Expense.objects.create(
            owner=self.bob,
            amount="95.00",
            description="Train ticket",
            category="Travel",
        )

    def test_expenses_are_scoped_to_authenticated_owner(self):
        response = self.client.get("/api/expenses/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["description"], "Coffee")

    def test_create_assigns_authenticated_owner(self):
        response = self.client.post(
            "/api/expenses/",
            {"amount": "8.25", "description": "Lunch", "category": "Food"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["owner"], "alice")
        self.assertEqual(Expense.objects.filter(owner=self.alice).count(), 2)

    def test_filters_search_and_ordering_are_enabled(self):
        response = self.client.get("/api/expenses/?category=Food&search=coffee&ordering=amount")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["description"], "Coffee")

    def test_login_returns_token(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            "/api/login/", {"username": "alice", "password": "pass1234"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
