import random
from faker import Faker
from backend.schemas.review import ReviewCreate

fake = Faker()

PRODUCTS = [
    ("EcoBrew Coffee Maker",    "Kitchen"),
    ("ZenFit Yoga Mat",         "Sports"),
    ("NovaSound Headphones",    "Electronics"),
    ("LunaGlow Skincare Set",   "Beauty"),
    ("SwiftKey Mechanical Keyboard", "Electronics"),
    ("AquaPure Water Bottle",   "Sports"),
    ("CloudStep Running Shoes", "Footwear"),
    ("BrightMind Study Lamp",   "Home"),
]

POSITIVE_PHRASES = [
    "Absolutely love this product!",
    "Exceeded my expectations in every way.",
    "Best purchase I've made this year.",
    "The quality is outstanding.",
    "Works perfectly straight out of the box.",
    "Incredible value for money.",
    "Fast delivery and great packaging.",
    "Highly recommend to everyone.",
]

NEGATIVE_PHRASES = [
    "Completely disappointed with this.",
    "Stopped working after just two weeks.",
    "The quality is much worse than advertised.",
    "Arrived damaged and customer support was unhelpful.",
    "Waste of money. Do not buy.",
    "Shipping took forever and the product is flimsy.",
    "Nothing like the photos on the website.",
    "Had to return it immediately.",
]

NEUTRAL_PHRASES = [
    "Decent product for the price.",
    "It does what it says, nothing more.",
    "Average quality but works fine.",
    "Shipping was slow but product is okay.",
    "Not bad but could be better.",
    "Some features are good, others not so much.",
    "It's okay. Probably won't buy again.",
    "Meets basic expectations.",
]

def generate_review() -> ReviewCreate:
    product_name, category = random.choice(PRODUCTS)
    star_rating = random.choices(
        [1, 2, 3, 4, 5],
        weights=[10, 10, 15, 30, 35]
    )[0]

    if star_rating >= 4:
        base = random.choice(POSITIVE_PHRASES)
    elif star_rating == 3:
        base = random.choice(NEUTRAL_PHRASES)
    else:
        base = random.choice(NEGATIVE_PHRASES)

    extra = fake.sentence(nb_words=random.randint(8, 20))
    review_text = f"{base} {extra}"

    return ReviewCreate(
        reviewer_name=fake.name(),
        product_name=product_name,
        product_category=category,
        star_rating=star_rating,
        review_text=review_text,
    )