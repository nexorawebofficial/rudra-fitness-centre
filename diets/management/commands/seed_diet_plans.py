from django.core.management.base import BaseCommand

from diets.models import DietCategory, DietPlan

HYDRATION_STANDARD = "2.5-3 litres of water daily. Add an extra glass for every 30-45 minutes of training."
HYDRATION_PERFORMANCE = "3.5-4 litres of water daily, plus electrolytes on heavy training days or in hot weather."

PLANS = [
    {
        "category": "Beginner Nutrition",
        "category_description": (
            "Simple, sustainable eating for members who are new to structured training. "
            "The goal is consistency with everyday food, not a complicated diet."
        ),
        "title": "Beginner Plan - Affordable",
        "breakfast": "Poha or vegetable daliya with a boiled egg or a bowl of sprouts, and a glass of milk.",
        "lunch": "2 roti, dal, a seasonal vegetable sabzi, curd, and a side salad.",
        "snack": "Roasted chana or a seasonal fruit (banana, apple, or guava).",
        "dinner": "Khichdi or dal-rice with mixed vegetables.",
        "hydration_notes": HYDRATION_STANDARD,
        "general_notes": (
            "Built entirely around everyday, budget-friendly, home-cooked food using local seasonal produce - "
            "no special ingredients required. When you're starting out, showing up consistently matters far "
            "more than eating anything fancy."
        ),
        "foods_to_include": "Seasonal vegetables, dal and legumes, eggs, milk, whole grains (roti, rice, daliya).",
        "foods_to_limit": "Bakery snacks and biscuits, sugary tea/coffee, fried street food.",
    },
    {
        "category": "Beginner Nutrition",
        "title": "Beginner Plan - Premium",
        "breakfast": "Oats or muesli with milk and mixed berries, plus 2 boiled eggs or a protein smoothie.",
        "lunch": "Grilled chicken, paneer, or tofu with quinoa or brown rice, a large mixed salad, and buttermilk.",
        "snack": "Greek yogurt with almonds and walnuts, or a protein bar.",
        "dinner": "Grilled fish, paneer, or soya chunks with sauteed vegetables and a small portion of brown rice.",
        "hydration_notes": HYDRATION_STANDARD,
        "general_notes": (
            "The same beginner-friendly structure as the affordable plan, built around higher-quality proteins "
            "and more variety of fruit and vegetables for members who'd rather start with more choice."
        ),
        "foods_to_include": "Lean proteins, whole grains, nuts and seeds, low-fat dairy, colourful vegetables.",
        "foods_to_limit": "Refined sugar, deep-fried food, excess added salt.",
    },
    {
        "category": "Performance Nutrition",
        "category_description": (
            "Higher-volume, protein-timed eating for experienced members training seriously and often. "
            "Built for consistent training loads, not for any specific medical goal."
        ),
        "title": "Professional Plan - Affordable",
        "breakfast": "3-egg omelette (or 4 egg whites + 1 whole egg) with vegetables, and 2 multigrain roti.",
        "lunch": "Chicken, rajma, or chana with brown rice or 3 roti, a large salad, and curd.",
        "snack": "Peanut butter on multigrain toast, or roasted chana with a banana.",
        "dinner": "Fish, soya chunks, or paneer with dal and sauteed vegetables.",
        "hydration_notes": HYDRATION_PERFORMANCE,
        "general_notes": (
            "Structured around eating protein every 3-4 hours to support a higher training volume, using "
            "affordable, widely available protein sources rather than supplements."
        ),
        "foods_to_include": "Eggs, legumes, seasonal vegetables, whole grains, peanut butter.",
        "foods_to_limit": "Processed/packaged meats, sugary drinks, excess refined carbs.",
    },
    {
        "category": "Performance Nutrition",
        "title": "Professional Plan - Premium",
        "breakfast": "Whey protein shake with oats and banana, plus a 3-egg omelette with avocado.",
        "lunch": "Grilled salmon or chicken breast, quinoa, roasted vegetables, and Greek yogurt.",
        "snack": "Protein shake with almonds, or cottage cheese with berries.",
        "dinner": "Lean steak, grilled fish, or tofu with sweet potato and leafy greens.",
        "hydration_notes": HYDRATION_PERFORMANCE + " Consider an electrolyte drink around long sessions.",
        "general_notes": (
            "A higher-cost version of the professional plan built around premium protein sources and optional "
            "supplement support (whey protein) for members who train frequently and prioritise convenience and "
            "recovery. Talk to your trainer before adding any new supplement."
        ),
        "foods_to_include": "Premium lean proteins, healthy fats (avocado, nuts), complex carbs, whey protein.",
        "foods_to_limit": "Alcohol, added sugar, low-quality fried food.",
    },

    # --- Weight Management: Beginner/Professional x Affordable/Premium ---
    {
        "category": "Weight Management",
        "title": "Weight Management - Beginner - Affordable",
        "breakfast": "Vegetable poha or upma with a boiled egg.",
        "lunch": "2 roti, dal, a vegetable sabzi, and a large salad (light on rice).",
        "snack": "Roasted chana or a small seasonal fruit.",
        "dinner": "Vegetable soup or a small bowl of dal with 1 roti.",
        "hydration_notes": "2.5-3 litres of water daily. Avoid sugary drinks entirely - they add up fast.",
        "general_notes": (
            "Built around portion control with everyday food rather than cutting out entire food groups. "
            "Consistent meal timing and not skipping meals matters more than eating anything special."
        ),
        "foods_to_include": "Vegetables, dal, roti, curd, seasonal fruit.",
        "foods_to_limit": "Fried snacks, sugary tea/coffee, refined carbs, late-night snacking.",
    },
    {
        "category": "Weight Management",
        "title": "Weight Management - Beginner - Premium",
        "breakfast": "Greek yogurt with mixed berries and chia seeds.",
        "lunch": "Grilled chicken or paneer salad with a small portion of quinoa.",
        "snack": "A protein shake or a small handful of almonds.",
        "dinner": "Grilled fish or tofu with steamed vegetables.",
        "hydration_notes": "3 litres of water daily; unsweetened green tea is fine in moderation.",
        "general_notes": (
            "Same portion-control approach as the affordable plan, built around higher-quality, more varied "
            "ingredients for members who'd rather start with more choice."
        ),
        "foods_to_include": "Lean protein, low-GI grains, leafy greens, low-fat dairy.",
        "foods_to_limit": "Processed sugar, alcohol, refined flour.",
    },
    {
        "category": "Weight Management",
        "title": "Weight Management - Professional - Affordable",
        "breakfast": "Egg-white omelette with vegetables and 1 multigrain roti.",
        "lunch": "Grilled chicken or rajma with a small portion of brown rice and a large salad.",
        "snack": "Buttermilk and roasted chana.",
        "dinner": "Dal and sauteed vegetables, kept light in the evening.",
        "hydration_notes": "3-3.5 litres of water daily.",
        "general_notes": (
            "Structured meal timing for members combining regular training with an active fat-loss phase, using "
            "affordable, everyday protein sources."
        ),
        "foods_to_include": "Lean protein, fibrous vegetables, legumes.",
        "foods_to_limit": "Added sugar, fried food, alcohol, processed snacks.",
    },
    {
        "category": "Weight Management",
        "title": "Weight Management - Professional - Premium",
        "breakfast": "Protein smoothie with spinach and mixed berries.",
        "lunch": "Grilled salmon or chicken breast with roasted vegetables.",
        "snack": "Cottage cheese with cucumber and herbs.",
        "dinner": "Grilled fish or tofu with a large mixed salad.",
        "hydration_notes": "3.5+ litres of water daily, plus electrolytes around longer training sessions.",
        "general_notes": (
            "Premium ingredients and optional supplement support for members in a structured fat-loss phase "
            "alongside serious training. Check with your trainer before making a significant change to your "
            "calorie intake."
        ),
        "foods_to_include": "Premium lean protein, healthy fats, fibrous vegetables.",
        "foods_to_limit": "Alcohol, added sugar, processed food.",
    },

    # --- Vegetarian Fitness: Beginner/Professional x Affordable/Premium ---
    {
        "category": "Vegetarian Fitness",
        "title": "Vegetarian Fitness - Beginner - Affordable",
        "breakfast": "Vegetable poha or moong dal chilla with curd.",
        "lunch": "2 roti, dal, a vegetable sabzi, curd, and salad.",
        "snack": "Roasted chana or a seasonal fruit.",
        "dinner": "Vegetable khichdi.",
        "hydration_notes": HYDRATION_STANDARD,
        "general_notes": "Everyday vegetarian staples, no special or hard-to-find ingredients required.",
        "foods_to_include": "Dal, paneer, curd, seasonal vegetables, whole grains.",
        "foods_to_limit": "Fried snacks, sugary drinks, excess refined carbs.",
    },
    {
        "category": "Vegetarian Fitness",
        "title": "Vegetarian Fitness - Beginner - Premium",
        "breakfast": "Oats with milk, mixed nuts, and fruit.",
        "lunch": "Grilled paneer or tofu with quinoa and a large salad.",
        "snack": "Greek yogurt with nuts.",
        "dinner": "Soya chunk curry with a small portion of brown rice.",
        "hydration_notes": HYDRATION_STANDARD,
        "general_notes": "The same vegetarian structure as the affordable plan, with more variety and higher-quality ingredients.",
        "foods_to_include": "Paneer, tofu, soya chunks, nuts, quinoa.",
        "foods_to_limit": "Refined sugar, deep-fried food.",
    },
    {
        "category": "Vegetarian Fitness",
        "title": "Vegetarian Fitness - Professional - Affordable",
        "breakfast": "Besan chilla with a paneer filling, plus sprouts.",
        "lunch": "Rajma or chana with brown rice or roti, a large salad, and curd.",
        "snack": "Peanut butter on multigrain toast, or roasted chana.",
        "dinner": "Paneer or soya chunks with dal and vegetables.",
        "hydration_notes": HYDRATION_PERFORMANCE,
        "general_notes": "Higher-protein, protein-timed vegetarian eating to support consistent training volume.",
        "foods_to_include": "Legumes, paneer, soya, nuts, whole grains.",
        "foods_to_limit": "Processed food, sugary drinks.",
    },
    {
        "category": "Vegetarian Fitness",
        "title": "Vegetarian Fitness - Professional - Premium",
        "breakfast": "Plant-protein shake with oats and banana, plus paneer bhurji.",
        "lunch": "Grilled paneer or tofu steak with quinoa and roasted vegetables.",
        "snack": "Plant-based protein shake with almonds.",
        "dinner": "Soya or tofu curry with sweet potato and leafy greens.",
        "hydration_notes": HYDRATION_PERFORMANCE + " Consider an electrolyte drink on heavy training days.",
        "general_notes": (
            "Premium plant-based protein sources and optional supplement support (plant protein powder) for "
            "vegetarian members training seriously and often."
        ),
        "foods_to_include": "Tofu, paneer, soya, quinoa, nuts, plant protein.",
        "foods_to_limit": "Alcohol, added sugar, fried food.",
    },

    # --- Muscle Building: Beginner/Professional x Affordable/Premium ---
    {
        "category": "Muscle Building",
        "title": "Muscle Building - Beginner - Affordable",
        "breakfast": "3 whole eggs with 2 multigrain toast, and a banana.",
        "lunch": "Chicken or rajma with rice, dal, and a salad.",
        "snack": "Peanut butter sandwich, or roasted chana with milk.",
        "dinner": "Paneer or chicken with roti and a vegetable sabzi.",
        "hydration_notes": "3 litres of water daily.",
        "general_notes": (
            "Focused on eating slightly more than maintenance, with a protein-rich meal roughly every 3-4 hours, "
            "using everyday ingredients."
        ),
        "foods_to_include": "Eggs, dal, milk, whole grains, peanut butter.",
        "foods_to_limit": "Sugary drinks, excess fried food.",
    },
    {
        "category": "Muscle Building",
        "title": "Muscle Building - Beginner - Premium",
        "breakfast": "Protein oats with milk, banana, and peanut butter.",
        "lunch": "Grilled chicken or paneer with rice and vegetables.",
        "snack": "Protein shake with fruit.",
        "dinner": "Fish or paneer with quinoa and salad.",
        "hydration_notes": "3-3.5 litres of water daily.",
        "general_notes": "Same muscle-building structure as the affordable plan, with higher-quality ingredients and shake convenience.",
        "foods_to_include": "Lean protein, complex carbs, healthy fats.",
        "foods_to_limit": "Excess added sugar, alcohol.",
    },
    {
        "category": "Muscle Building",
        "title": "Muscle Building - Professional - Affordable",
        "breakfast": "4-egg omelette with 3 multigrain roti, and a glass of milk.",
        "lunch": "Chicken or rajma with rice, dal, and salad.",
        "snack": "Peanut butter sandwich, banana, and milk.",
        "dinner": "Paneer, chicken, or fish with rice/roti and a vegetable sabzi.",
        "hydration_notes": HYDRATION_PERFORMANCE,
        "general_notes": (
            "Higher-calorie eating spread across 5-6 meals a day to support a serious training volume, built "
            "around affordable staple foods."
        ),
        "foods_to_include": "Eggs, dal, milk, whole grains.",
        "foods_to_limit": "Sugary drinks, junk food, alcohol.",
    },
    {
        "category": "Muscle Building",
        "title": "Muscle Building - Professional - Premium",
        "breakfast": "Whey protein shake with oats, peanut butter, and banana.",
        "lunch": "Grilled chicken or salmon with rice, avocado, and vegetables.",
        "snack": "Protein shake with nuts (or a mass gainer, only as advised by your trainer).",
        "dinner": "Lean steak, fish, or paneer with sweet potato and leafy greens.",
        "hydration_notes": HYDRATION_PERFORMANCE + " Consider electrolytes around longer training sessions.",
        "general_notes": (
            "Premium protein sources and optional supplement support (whey protein, or a mass gainer) for "
            "members focused on serious muscle building. Discuss any new supplement with your trainer first."
        ),
        "foods_to_include": "Premium lean protein, complex carbs, healthy fats, whey protein.",
        "foods_to_limit": "Alcohol, excess added sugar, low-quality processed food.",
    },
]


class Command(BaseCommand):
    help = (
        "Seeds Beginner/Professional x Affordable/Premium diet plans across the Beginner Nutrition, "
        "Performance Nutrition, Weight Management, Vegetarian Fitness, and Muscle Building categories."
    )

    def handle(self, *args, **options):
        created_count = 0
        category_cache = {}

        for entry in PLANS:
            category_name = entry["category"]
            if category_name not in category_cache:
                category, _ = DietCategory.objects.get_or_create(
                    name=category_name,
                    defaults={"description": entry.get("category_description", "")},
                )
                category_cache[category_name] = category
            category = category_cache[category_name]

            plan, created = DietPlan.objects.get_or_create(
                category=category,
                title=entry["title"],
                defaults={
                    "breakfast": entry["breakfast"],
                    "lunch": entry["lunch"],
                    "snack": entry["snack"],
                    "dinner": entry["dinner"],
                    "hydration_notes": entry["hydration_notes"],
                    "general_notes": entry["general_notes"],
                    "foods_to_include": entry["foods_to_include"],
                    "foods_to_limit": entry["foods_to_limit"],
                    "is_published": True,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded diet content: {created_count} new plan(s) created (existing ones left untouched).",
        ))
