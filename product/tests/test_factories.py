from django.test import TestCase

from product.tests.factories import ProductFactory, CategoryFactory


class TestProductFactory(TestCase):
    def test_product_factory_creates_fields(self):
        product = ProductFactory()

        self.assertTrue(product.price)
        self.assertTrue(product.category)
        self.assertTrue(product.title)

    def test_product_factory_accepts_different_values(self):
        title = "Product Title"
        description = "Product Description"
        price = 99.87
        active = False

        product = ProductFactory(
            title=title, description=description, price=price, active=active
        )

        self.assertEqual(product.title, title, msg="Product has wrong title")
        self.assertEqual(
            product.description, description, msg="Product has wrong description"
        )
        self.assertEqual(product.price, price, msg="Product has wrong price")
        self.assertEqual(product.active, active, msg="Product has wrong active status")

    def test_product_factory_add_categories(self):
        category_one = CategoryFactory(title="First Title")
        category_two = CategoryFactory(title="Second Title")
        category_three = CategoryFactory(title="Third Title")

        product = ProductFactory(category=[category_three, category_one])

        product_categories = []
        for cat in product.category.all():
            product_categories.append(cat.title)

        self.assertIn(
            category_one.title,
            product_categories,
            msg="Expected category title not found in product categories",
        )
        self.assertIn(
            category_three.title,
            product_categories,
            msg="Expected category title not found in product categories",
        )
        self.assertNotIn(
            category_two.title,
            product_categories,
            msg="Not expected category title found in product categories",
        )

    def test_product_factory_not_created_return(self):
        category_one = CategoryFactory(title="First Product")

        product = ProductFactory.build(
            category=[
                category_one,
            ]
        )

        self.assertFalse(product.id, msg="An unexpected ID was found.")


class TestCategoryFactory(TestCase):
    def test_category_factory_creates_fields(self):
        category = CategoryFactory(active=True)

        self.assertTrue(category.title)
        self.assertTrue(category.slug)
        self.assertTrue(category.description)
        self.assertTrue(category.active)

    def test_category_factory_accepts_different_values(self):
        title = "Category Title"
        slug = "category-title"
        description = "Category description"
        active = False

        category = CategoryFactory(
            title=title, description=description, slug=slug, active=active
        )

        self.assertEqual(title, category.title, msg="Category has wrong title.")
        self.assertEqual(slug, category.slug, msg="Category has wrong slug.")
        self.assertEqual(
            description, category.description, msg="Category has wrong description."
        )
        self.assertEqual(
            active, category.active, msg="Category has wrong active status."
        )
