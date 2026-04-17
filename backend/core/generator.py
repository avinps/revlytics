import random
import time
from faker import Faker
from backend.schemas.review import ReviewCreate

fake = Faker()

PRODUCTS = [
    ("EcoBrew Coffee Maker",         "Kitchen"),
    ("ZenFit Yoga Mat",              "Sports"),
    ("NovaSound Headphones",         "Electronics"),
    ("LunaGlow Skincare Set",        "Beauty"),
    ("SwiftKey Mechanical Keyboard", "Electronics"),
    ("AquaPure Water Bottle",        "Sports"),
    ("CloudStep Running Shoes",      "Footwear"),
    ("BrightMind Study Lamp",        "Home"),
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
    "Terrible experience from start to finish.",
    "Broke on first use. Absolute garbage.",
    "Do not buy this. Complete waste of money.",
    "Worst product I have ever purchased.",
]

NEUTRAL_PHRASES = [
    "Decent product for the price.",
    "It does what it says, nothing more.",
    "Average quality but works fine.",
    "Shipping was slow but product is okay.",
    "Not bad but could be better.",
    "Some features are good, others not so much.",
    "It is okay. Probably won't buy again.",
    "Meets basic expectations.",
]

# ── crisis mode state ─────────────────────────────────────
_crisis_mode     = False
_crisis_count    = 0
_crisis_max      = 0
_normal_count    = 0
_normal_until    = 0
# ─────────────────────────────────────────────────────────

def _should_trigger_crisis() -> bool:
    global _crisis_mode, _normal_until
    if _crisis_mode:
        return True
    if time.time() < _normal_until:
        return False
    # 15% chance of triggering a crisis every review
    return random.random() < 0.40

def _update_crisis_state():
    global _crisis_mode, _crisis_count, _crisis_max, _normal_count, _normal_until

    if not _crisis_mode:
        _crisis_mode  = True
        _crisis_count = 0
        _crisis_max   = random.randint(8, 20)
        return

    _crisis_count += 1
    if _crisis_count >= _crisis_max:
        _crisis_mode  = False
        _crisis_count = 0
        _normal_until = time.time() + random.randint(15, 40)

def generate_review() -> ReviewCreate:
    global _crisis_mode

    in_crisis = _should_trigger_crisis()
    if in_crisis:
        _update_crisis_state()

    product_name, category = random.choice(PRODUCTS)

    if in_crisis:
        star_rating = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        base        = random.choice(NEGATIVE_PHRASES)
    else:
        star_rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[5, 8, 12, 30, 45]
        )[0]
        if star_rating >= 4:
            base = random.choice(POSITIVE_PHRASES)
        elif star_rating == 3:
            base = random.choice(NEUTRAL_PHRASES)
        else:
            base = random.choice(NEGATIVE_PHRASES)

    review_text = base

    return ReviewCreate(
        reviewer_name=fake.name(),
        product_name=product_name,
        product_category=category,
        star_rating=star_rating,
        review_text=review_text,
    )