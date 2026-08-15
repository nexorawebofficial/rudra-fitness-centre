from django.test import TestCase
from django.urls import reverse

from diets.models import DietCategory, DietPlan


class DietNutritionViewTests(TestCase):
    def setUp(self):
        self.category = DietCategory.objects.create(name='Weight Management', description='Balanced nutrition.')
        self.published_plan = DietPlan.objects.create(
            category=self.category, title='Beginner Plan', breakfast='Oats',
            foods_to_include='Vegetables', foods_to_limit='Sugary drinks', is_published=True,
        )
        self.unpublished_plan = DietPlan.objects.create(
            category=self.category, title='Draft Plan', breakfast='Draft breakfast', is_published=False,
        )

    def test_diet_nutrition_overview_lists_category(self):
        response = self.client.get(reverse('diet_nutrition'))
        self.assertContains(response, 'Weight Management')
        self.assertContains(response, 'Disclaimer')

    def test_overview_only_counts_published_plans(self):
        response = self.client.get(reverse('diet_nutrition'))
        self.assertContains(response, '1 plan available')

    def test_category_detail_lists_only_published_plans(self):
        response = self.client.get(reverse('diet_category_detail', args=[self.category.slug]))
        self.assertContains(response, 'Beginner Plan')
        self.assertNotContains(response, 'Draft Plan')

    def test_published_plan_detail_shows_full_content(self):
        response = self.client.get(reverse('diet_plan_detail', args=[self.published_plan.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oats')
        self.assertContains(response, 'Vegetables')
        self.assertContains(response, 'Sugary drinks')
        self.assertContains(response, 'Disclaimer')

    def test_unpublished_plan_detail_returns_404(self):
        response = self.client.get(reverse('diet_plan_detail', args=[self.unpublished_plan.pk]))
        self.assertEqual(response.status_code, 404)

    def test_unknown_category_slug_returns_404(self):
        response = self.client.get(reverse('diet_category_detail', args=['not-a-real-category']))
        self.assertEqual(response.status_code, 404)
