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
        product_one = ProductFactory(title='First Product')
        product_two = ProductFactory(title='Second Product')
        product_three = ProductFactory(title='Third Product')

        order = OrderFactory(product=[product_one, product_three])
        product_list = list()
        for product in order.product.all():
            product_list.append(product.title)

        self.assertIn(
            product_one.title,
            product_list,
            msg='Expected product title not found in the order.'
        )

        self.assertIn(
            product_three.title,
            product_list,
            msg='Expected product title not found in the order.'
        )

        self.assertNotIn(
            product_two.title,
            product_list,
            msg='Unexpected product title found in the order.'
        )

        self.assertEqual(
            2,
            len(product_list),
            msg='Wrong number of products found in the order.'
        )

    def test_order_factory_not_created_return(self):
        product_one = ProductFactory(title='First Product')

        order = OrderFactory.build(product=[product_one,])

        self.assertFalse(order.id, msg='An unexpected ID was found.')


class UserFactoryTest(TestCase):
    def test_user_factory_creates_fields(self):
        user = UserFactory()
        self.assertTrue(
            user.username, msg="User's Username is equivalent to False")
        self.assertTrue(user.email, msg="User's E-mail is equivalent to False")
