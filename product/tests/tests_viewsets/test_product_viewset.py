import json
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.urls import reverse

from product.models.category import Category
from product.tests.factories import CategoryFactory


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="books")

    def test_get_all_categories(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Unexpected status code returned.",
        )

        category_data = json.loads(response.content)["results"][0]

        self.assertEqual(category_data["title"], self.category.title)

    def test_create_category(self):

        data = json.dumps(
            {
                "title": "Tech",
                "slug": "tech-slug",
            }
        )

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Unexpected status code returned.",
        )

        created_category = Category.objects.get(title="Tech")
        self.assertEqual(created_category.title, "Tech")
        self.assertEqual(created_category.slug, "tech-slug")
