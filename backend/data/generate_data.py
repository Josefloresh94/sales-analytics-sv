# ==============================================================================
# generate_data.py
# Synthetic sales data generator for El Salvador market (2024)
#
# This script creates a realistic dataset of 2,000 sales records using
# Salvadoran products, branches, and business logic.
# The output is a CSV file used for data analysis in later stages.
# ==============================================================================
# --- IMPORTS ------------------------------------------------------------------
# random: Python's built-in module for random choices and numbers.
import random

# datetime, timedelta: used to generate random dates within the year 2024.
#   - datetime: represents a specific point in time (year, month, day...)
#   - timedelta: represents a duration (e.g. "30 days later")
from datetime import datetime, timedelta

# numpy: numerical computing library. We use it only to set a random seed,
#        which ensures we get the same "random" data every time we run the script.
import numpy as np

# pandas: main library for data manipulation. We use it to create the DataFrame
#         and export it to CSV at the end.
import pandas as pd

# Faker: library that generates fake but realistic data (names, dates, etc.)
#        'es_MX' means we use Latin American Spanish locale.
from faker import Faker

# --- SETUP --------------------------------------------------------------------
fake = Faker("es_MX")
# Seeds guarantee reproducibility: if we run the script again,
# we get the exact same 2,000 records. Critical for data analysis
# because results must be consistent between runs.
np.random.seed(42)
random.seed(42)

# ==============================================================================
# CATALOGS
# These are the "master data" of the business — the fixed reference lists
# that don't change between sales. In a real database, these would be
# separate tables (branches, products, etc.).
# ==============================================================================

# List of physical store locations across El Salvador.
# Type hint: list of dicts where keys are str and values are int or str.
# This tells the linter exactly what data types to expect, avoiding warnings.
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

# Product catalog with their base prices in USD (El Salvador uses USD).
# Type hint includes float because prices are decimal numbers.
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

# Available payment methods. El Salvador is one of the few countries
# where Bitcoin is legal tender, so we include it as a realistic option.
PAYMENT_METHODS: list[str] = [
    "Cash",
    "Debit card",
    "Credit card",
    "Bitcoin",
    "Transfer",
]
# Probability weights for each payment method (must sum to 1.0).
# Cash is most common (50%), followed by debit (25%), etc.
# random.choices() uses these weights to simulate realistic payment behavior.
PAYMENT_WEIGHTS: list[float] = [0.50, 0.25, 0.15, 0.05, 0.05]


# ==============================================================================
# GENERATOR FUNCTION
# ==============================================================================
def generate_sales(n: int = 2000) -> pd.DataFrame:
    """
    Generates n synthetic sales records for El Salvador market.

    Each record simulates one real transaction: which product was sold,
    at which branch, on which date, with what discount and payment method.

    Args:
        n: number of sales records to generate (default: 2000)

    Returns:
        pd.DataFrame: a table where each row is one sale transaction
    """

    # List that will accumulate all records before converting to DataFrame.
    # It's faster to append to a list and convert once at the end
    # than to append rows to a DataFrame one by one.
    records = []

    # All sales happen within the year 2024, starting from January 1st.
    start_date = datetime(2024, 1, 1)

    for i in range(n):
        # --- Pick random product and branch from our catalogs ---
        product: dict[str, int | str | float] = random.choice(PRODUCTS)
        branch: dict[str, int | str] = random.choice(BRANCHES)

        # --- Generate a random date within 2024 ---
        # timedelta(days=X) adds X days to the start date.
        # random.randint(0, 364) gives us any day in the year.
        date = start_date + timedelta(days=random.randint(0, 364))

        # --- Business logic: quantity and discounts ---
        quantity = random.randint(1, 20)

        # 60% of sales have no discount (four 0.0 values out of seven options).
        # The rest have 5%, 10% or 15% off — realistic promotional pricing.
        discount = random.choice([0.0, 0.0, 0.0, 0.0, 0.05, 0.10, 0.15])

        # --- Price calculations ---
        # float() cast is explicit here to avoid linter warnings.
        # Without it, the linter sees product["price"] as "object" (unknown type)
        # because the dict type hint allows int | str | float.
        price: float = float(product["price"])

        # Apply discount: if discount=0.10, then (1 - 0.10) = 0.90 → 10% off
        # round(..., 2) keeps exactly 2 decimal places → clean dollar amounts
        final_price: float = round(price * (1 - discount), 2)

        # Total = price after discount × number of units sold
        total: float = round(final_price * quantity, 2)

        # --- Build the record as a dictionary ---
        # Each key will become a column in the final DataFrame.
        records.append(
            {
                "sale_id": i + 1,  # unique ID starting at 1
                "date": date.strftime("%Y-%m-%d"),  # formatted as "2024-05-20"
                "month": date.month,  # integer 1-12
                "weekday": date.strftime("%A"),  # "Monday", "Tuesday", etc.
                "branch_id": branch["id"],
                "branch_name": branch["name"],
                "department": branch["department"],
                "product_id": product["id"],
                "product_name": product["name"],
                "category": product["category"],
                "unit_price": price,  # original price before discount
                "discount": discount,  # 0.0, 0.05, 0.10, or 0.15
                "final_price": final_price,  # price after discount
                "quantity": quantity,  # units sold
                "total": total,  # final_price × quantity
                "payment_method": random.choices(  # weighted random payment method
                    PAYMENT_METHODS, weights=PAYMENT_WEIGHTS
                )[0],  # [0] because choices() returns a list
                "customer_id": random.randint(
                    1, 500
                ),  # 500 unique customers in the system
            }
        )

    # Convert the list of dicts into a pandas DataFrame.
    # Each dict becomes a row, each key becomes a column.
    return pd.DataFrame(records)


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

# This block only runs when we execute this file directly:
#   python backend/data/generate_data.py
#
# It does NOT run when another script imports this file (e.g. import generate_data).
# This is a Python best practice for scripts that can also be used as modules.
if __name__ == "__main__":
    print("Generating dataset...")
    df = generate_sales(2000)

    # Save to CSV in the data folder.
    # index=False prevents pandas from adding an extra numeric column (0,1,2...)
    # since we already have our own sale_id column.
    output_path = "backend/data/sales_sv_2024.csv"
    df.to_csv(output_path, index=False)

    # Print a summary to confirm everything looks correct
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
