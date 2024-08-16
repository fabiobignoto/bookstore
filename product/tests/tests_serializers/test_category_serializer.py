from rest_framework.test import APITestCase

from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


class TestCategorytSerializer(APITestCase):
    def test_category_serializer_creates_valid_category(self):

        title = "My Category"
        description = "My description"
        slug = "my-category"
        active_status = True

        serializer = CategorySerializer(
            data={
                "title": title,
                "description": description,
                "slug": slug,
                "active": active_status,
            }
        )

        self.assertTrue(serializer.is_valid(), msg="Serializer was not valid.")

        serializer.save()
        category = Category.objects.get(slug=slug)

        self.assertEqual(category.title, title, msg="Unexpected category title found.")

        self.assertEqual(category.slug, slug, msg="Unexpected category slug found.")

        self.assertEqual(
            category.description,
            description,
            msg="Unexpected category description found.",
        )

        self.assertEqual(
            category.active,
            active_status,
            msg="Unexpected category active status found.",
        )
