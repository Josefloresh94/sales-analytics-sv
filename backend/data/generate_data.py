import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("es_MX")
np.random.seed(42)
random.seed(42)

# ── CATALOGS ────────────────────────────────────────────────────────

BRANCHES: list[dict[str, int | str]] = [
    {"id": 1, "name": "San Salvador Centro", "department": "San Salvador"},
    {"id": 2, "name": "Santa Ana", "department": "Santa Ana"},
    {"id": 3, "name": "San Miguel", "department": "San Miguel"},
    {"id": 4, "name": "Soyapango", "department": "San Salvador"},
    {"id": 5, "name": "Metrocentro", "department": "San Salvador"},
    {"id": 6, "name": "Usulután", "department": "Usulután"},
    {"id": 7, "name": "La Libertad", "department": "La Libertad"},
    {"id": 8, "name": "Chalatenango", "department": "Chalatenango"},
]

PRODUCTS: list[dict[str, int | str | float]] = [
    {
        "id": 1,
        "name": "Pupusas de queso",
        "category": "Traditional Food",
        "price": 0.50,
    },
    {
        "id": 2,
        "name": "Pupusas de frijol",
        "category": "Traditional Food",
        "price": 0.50,
    },
    {
        "id": 3,
        "name": "Tamales de elote",
        "category": "Traditional Food",
        "price": 1.00,
    },
    {"id": 4, "name": "Yuca frita", "category": "Traditional Food", "price": 2.50},
    {"id": 5, "name": "Atol de elote", "category": "Beverages", "price": 1.00},
    {"id": 6, "name": "Kolachampán", "category": "Beverages", "price": 0.75},
    {"id": 7, "name": "Café salvadoreño", "category": "Beverages", "price": 1.50},
    {"id": 8, "name": "Fresco de tamarindo", "category": "Beverages", "price": 0.75},
    {"id": 9, "name": "Camisa guayabera", "category": "Clothing", "price": 18.00},
    {"id": 10, "name": "Hamaca artesanal", "category": "Handicrafts", "price": 35.00},
    {"id": 11, "name": "Jarrito de barro", "category": "Handicrafts", "price": 8.00},
    {"id": 12, "name": "Canasta de palma", "category": "Handicrafts", "price": 12.00},
    {"id": 13, "name": "Aceite vegetal 1L", "category": "Groceries", "price": 2.80},
    {"id": 14, "name": "Frijoles rojos 1lb", "category": "Groceries", "price": 1.20},
    {"id": 15, "name": "Arroz blanco 1lb", "category": "Groceries", "price": 0.90},
    {"id": 16, "name": "Crema salvadoreña", "category": "Dairy", "price": 1.50},
    {"id": 17, "name": "Queso duro blando", "category": "Dairy", "price": 3.50},
    {"id": 18, "name": "Curtido en frasco", "category": "Groceries", "price": 2.00},
]

PAYMENT_METHODS: list[str] = [
    "Cash",
    "Debit card",
    "Credit card",
    "Bitcoin",
    "Transfer",
]
PAYMENT_WEIGHTS: list[float] = [0.50, 0.25, 0.15, 0.05, 0.05]

# ── GENERATOR ───────────────────────────────────────────────────────


def generate_sales(n: int = 2000) -> pd.DataFrame:
    records = []
    start_date = datetime(2024, 1, 1)

    for i in range(n):
        product: dict[str, int | str | float] = random.choice(PRODUCTS)
        branch: dict[str, int | str] = random.choice(BRANCHES)
        date = start_date + timedelta(days=random.randint(0, 364))
        quantity = random.randint(1, 20)
        discount = random.choice([0.0, 0.0, 0.0, 0.0, 0.05, 0.10, 0.15])
        price: float = float(product["price"])
        final_price: float = round(price * (1 - discount), 2)
        total: float = round(final_price * quantity, 2)

        records.append(
            {
                "sale_id": i + 1,
                "date": date.strftime("%Y-%m-%d"),
                "month": date.month,
                "weekday": date.strftime("%A"),
                "branch_id": branch["id"],
                "branch_name": branch["name"],
                "department": branch["department"],
                "product_id": product["id"],
                "product_name": product["name"],
                "category": product["category"],
                "unit_price": price,
                "discount": discount,
                "final_price": final_price,
                "quantity": quantity,
                "total": total,
                "payment_method": random.choices(
                    PAYMENT_METHODS, weights=PAYMENT_WEIGHTS
                )[0],
                "customer_id": random.randint(1, 500),
            }
        )

    return pd.DataFrame(records)


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating dataset...")
    df = generate_sales(2000)

    output_path = "backend/data/sales_sv_2024.csv"
    df.to_csv(output_path, index=False)

    print(f"\n✅ Dataset generated: {len(df)} records")
    print(f"📁 Saved at: {output_path}")
    print("\n📊 Preview:")
    print(df.head())
    print("\n📈 Summary:")
    print(f"   Total revenue:    ${df['total'].sum():,.2f}")
    print(f"   Average ticket:   ${df['total'].mean():.2f}")
    print(f"   Branches:         {df['branch_name'].nunique()}")
    print(f"   Unique products:  {df['product_name'].nunique()}")
    print(f"   Period:           {df['date'].min()} → {df['date'].max()}")
