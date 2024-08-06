from django.test import TestCase
from .factories import OrderFactory, UserFactory

from product.tests.factories import ProductFactory


class OrderFactoryTest(TestCase):
    def test_order_factory_creates_fields(self):

        order = OrderFactory()
        self.assertTrue(order.user, msg="Order's User is equivalent to False.")
        self.assertTrue(
            order.product, msg="Order's Product is equivalent to False.")

    def test_order_factory_add_products(self):
        product_one = ProductFactory()
        product_two = ProductFactory()
        order = OrderFactory(product_one, product_two)
        ...


class UserFactoryTest(TestCase):
    def test_user_factory_creates_fields(self):
        user = UserFactory()
        self.assertTrue(
            user.username, msg="User's Username is equivalent to False")
        self.assertTrue(user.email, msg="User's E-mail is equivalent to False")
