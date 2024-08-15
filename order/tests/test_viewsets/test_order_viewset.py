import json
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from django.urls import reverse

from product.tests.factories import CategoryFactory, ProductFactory
from order.tests.factories import OrderFactory, UserFactory

from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="Technology")
        self.product = ProductFactory(
            title="Mouse", price=100, category=[self.category]
        )

        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.order = OrderFactory(product=[self.product])

    def test_order(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Unexpected status code returned.",
        )

        order_data = json.loads(response.content)["results"][0]["product"][0]
        self.assertEqual(order_data["title"], self.product.title)
        self.assertEqual(order_data["price"], self.product.price)
        self.assertEqual(order_data["active"], self.product.active)
        self.assertEqual(order_data["category"][0]["title"], self.category.title)

    def test_create_order(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = json.dumps({"products_id": [self.product.id], "user": self.user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Unexpected status code returned.",
        )

        created_order = Order.objects.get(user=self.user)

        self.assertEqual(
            len(created_order.product.all()),
            1,
            msg="Unexpected number of products in the created order.",
        )

        self.assertEqual(
            created_order.product.all()[0].title,
            self.product.title,
            msg="Unexpected Product found in the created order.",
        )

        self.assertEqual(
            created_order.user.username,
            self.user.username,
            msg="Unexpected User found in the created order.",
        )
