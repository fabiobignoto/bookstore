
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from order.models.order import Order
from order.serializers.order_serializer import OrderSerializer
from product.tests.factories import CategoryFactory, ProductFactory


class TestCategorytSerializer (APITestCase):
    def test_order_serializer_creates_valid_order(self):
        user = User.objects.create_user(
            username='my-username',
            password='my-password',
            email='my-email@server.com')

        category_one = CategoryFactory()

        product_one = ProductFactory(category=[category_one])
        product_two = ProductFactory(category=[category_one])

        product_three = ProductFactory(category=[category_one])

        products_id = [product_one.id, product_three.id]

        serializer = OrderSerializer(
            data={
                'products_id': products_id,
                'user': user.id
            }
        )

        self.assertTrue(serializer.is_valid(), msg='Serializer was not valid.')

        order_from_serializer = serializer.save()

        order = Order.objects.get(id=order_from_serializer.id)

        self.assertIn(
            product_one, order.product.all(),
            msg='Expected order not found')

        self.assertNotIn(
            product_two, order.product.all(),
            msg='Expected order not found')

        self.assertIn(
            product_three, order.product.all(),
            msg='Expected order not found')
