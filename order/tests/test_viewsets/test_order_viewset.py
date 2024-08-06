import json
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.urls import reverse

from product.tests.factories import CategoryFactory, ProductFactory
from order.tests.factories import OrderFactory, UserFactory

from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='Technology')
        self.product = ProductFactory(
            title='Mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'}))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg='Unexpected status code returned.')

        order_data = json.loads(response.content)[0]
        self.assertEqual(order_data['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]
                         ['active'], self.product.active)
        self.assertEqual(order_data['product'][0]
                         ['category'][0]['title'], self.category.title)

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({
            'products_id': [product.id],
            'user': user.id
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            format='application/json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg='Unexpected status code returned.'

        )

        created_order = Order.objects.get(user=user)
