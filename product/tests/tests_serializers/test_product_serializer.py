from rest_framework.test import APITestCase

from product.models.category import Category
from product.models.product import Product

from product.serializers.product_serializer import ProductSerializer


class TestProductSerializer(APITestCase):
    def test_product_serializer_creates_valid_product(self):

        category_one = Category.objects.create(
            title="My first category", slug="my-first-category", active=True
        )

        category_two = Category.objects.create(
            title="My second category", slug="my-second-category", active=True
        )

        category_three = Category.objects.create(
            title="My third category", slug="my-third-category", active=True
        )

        categories_id = [category_one.id, category_three.id]

        title = "My Product"
        description = "My description"
        price = 123
        active_status = True

        serializer = ProductSerializer(
            data={
                "title": title,
                "description": description,
                "price": price,
                "active": active_status,
                "categories_id": categories_id,
            }
        )

        self.assertTrue(serializer.is_valid(), msg="Serializer was not valid.")

        serializer.save()

        product = Product.objects.get(title=title)

        product_categories_list = list()
        for category in product.category.all():
            product_categories_list.append(category.title)

        self.assertEqual(product.title, title, msg="Unexpected product title found.")
        self.assertEqual(
            product.description,
            description,
            msg="Unexpected product description found.",
        )
        self.assertEqual(product.price, price, msg="Unexpected product price found.")
        self.assertEqual(
            product.active, active_status, msg="Unexpected product active status found."
        )

        self.assertEqual(
            len(product.category.all()), 2, msg="Unexpected product category length."
        )

        self.assertIn(
            category_one.title,
            product_categories_list,
            msg="Expected category title not found.",
        )

        self.assertIn(
            category_three.title,
            product_categories_list,
            msg="Expected category title not found.",
        )

        self.assertNotIn(
            category_two.title,
            product_categories_list,
            msg="Unexpected category title found.",
        )
