import csv
import random
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

random.seed(42)

ACCOUNTS = {
    "4000": {"name": "Umsatzerloese Dienstleistungen", "type": "revenue", "statement": "guv", "vat_rate": 0.19},
    "4100": {"name": "Umsatzerloese Produkte", "type": "revenue", "statement": "guv", "vat_rate": 0.19},
    "4200": {"name": "Sonstige betriebliche Ertraege", "type": "revenue", "statement": "guv", "vat_rate": 0.19},
    "5000": {"name": "Wareneinsatz", "type": "expense", "statement": "guv", "vat_rate": 0.19},
    "5100": {"name": "Marketingkosten", "type": "expense", "statement": "guv", "vat_rate": 0.19},
    "5200": {"name": "Software und Lizenzen", "type": "expense", "statement": "guv", "vat_rate": 0.19},
    "5300": {"name": "Miete", "type": "expense", "statement": "guv", "vat_rate": 0.19},
    "5400": {"name": "Reisekosten", "type": "expense", "statement": "guv", "vat_rate": 0.07},
    "1000": {"name": "Bank", "type": "asset", "statement": "bilanz", "vat_rate": 0.0},
    "1200": {"name": "Forderungen aus Lieferungen und Leistungen", "type": "asset", "statement": "bilanz", "vat_rate": 0.0},
    "1600": {"name": "Vorsteuer", "type": "asset", "statement": "bilanz", "vat_rate": 0.0},
    "1400": {"name": "Betriebs- und Geschaeftsausstattung", "type": "asset", "statement": "bilanz", "vat_rate": 0.0},
    "2000": {"name": "Verbindlichkeiten aus Lieferungen und Leistungen", "type": "liability", "statement": "bilanz", "vat_rate": 0.0},
    "3000": {"name": "Eigenkapital", "type": "equity", "statement": "bilanz", "vat_rate": 0.0},
    "1776": {"name": "Umsatzsteuer", "type": "liability", "statement": "bilanz", "vat_rate": 0.0},
}

CUSTOMERS = [
    "Alpha GmbH", "Beta Solutions", "City Bakery", "Delta Studio", "Eco Store",
    "Futura Labs", "Green Office", "Havel Hotel", "Innotech AG", "Juno Media"
]

VENDORS = [
    "Adobe", "AWS", "Bahn", "CoWorking Berlin", "Meta Ads",
    "Microsoft", "Notebookshop", "Office Depot", "Telekom", "Travel Partner"
]

REVENUE_BOOKINGS = [
    {"account": "4000", "category": "service", "text": "Webprojekt", "payment": "bank_transfer", "cost_center": "consulting", "amount_range": (800, 4500), "counter_account": "1000", "invoice_probability": 0.75},
    {"account": "4100", "category": "product", "text": "Softwarelizenz", "payment": "bank_transfer", "cost_center": "software", "amount_range": (150, 1800), "counter_account": "1200", "invoice_probability": 1.0},
    {"account": "4200", "category": "other_income", "text": "Workshop", "payment": "card", "cost_center": "training", "amount_range": (250, 2200), "counter_account": "1000", "invoice_probability": 0.6},
]

EXPENSE_BOOKINGS = [
    {"account": "5000", "category": "cogs", "text": "Wareneinkauf", "payment": "bank_transfer", "cost_center": "operations", "amount_range": (120, 2200), "counter_account": "2000", "invoice_probability": 1.0},
    {"account": "5100", "category": "marketing", "text": "Onlinekampagne", "payment": "card", "cost_center": "marketing", "amount_range": (80, 900), "counter_account": "1000", "invoice_probability": 0.9},
    {"account": "5200", "category": "software", "text": "SaaS Abo", "payment": "card", "cost_center": "it", "amount_range": (20, 300), "counter_account": "1000", "invoice_probability": 1.0},
    {"account": "5300", "category": "rent", "text": "Buero Miete", "payment": "bank_transfer", "cost_center": "admin", "amount_range": (900, 1400), "counter_account": "1000", "invoice_probability": 1.0},
    {"account": "5400", "category": "travel", "text": "Dienstreise", "payment": "cash", "cost_center": "sales", "amount_range": (40, 350), "counter_account": "1000", "invoice_probability": 0.7},
]


def dec(x):
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def random_date(year):
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


def maybe_missing(value, probability=0.08):
    return "" if random.random() < probability else value


def create_booking(i, year):
    booking_kind = random.choices(["revenue", "expense"], weights=[0.45, 0.55], k=1)[0]
    template = random.choice(REVENUE_BOOKINGS if booking_kind == "revenue" else EXPENSE_BOOKINGS)
    account = ACCOUNTS[template["account"]]
    counter = ACCOUNTS[template["counter_account"]]
    booking_date = random_date(year)
    amount_net = dec(random.uniform(*template["amount_range"]))
    vat_rate = Decimal(str(account["vat_rate"]))
    vat_amount = dec(amount_net * vat_rate)
    amount_gross = dec(amount_net + vat_amount)
    paid = random.random() < 0.72
    due_date = booking_date + timedelta(days=random.choice([7, 14, 30]))
    payment_date = booking_date + timedelta(days=random.randint(0, 35)) if paid else None
    quantity = random.randint(1, 12)
    unit_price = dec(amount_net / quantity)
    doc_type = random.choice(["invoice", "receipt", "credit_note"]) if random.random() < 0.08 else ("invoice" if random.random() < template["invoice_probability"] else "receipt")
    partner = random.choice(CUSTOMERS if booking_kind == "revenue" else VENDORS)
    recurring = template["category"] in {"software", "rent"}
    cash_effective = template["payment"] in {"bank_transfer", "card", "cash"}

    return {
        "booking_id": i,
        "booking_date": booking_date.isoformat(),
        "due_date": due_date.isoformat(),
        "payment_date": payment_date.isoformat() if payment_date else "",
        "fiscal_year": year,
        "month": booking_date.month,
        "quarter": f"Q{((booking_date.month - 1) // 3) + 1}",
        "document_number": maybe_missing(f"DOC-{year}-{i:04d}", 0.05),
        "document_type": doc_type,
        "booking_type": booking_kind,
        "account_code": template["account"],
        "account_name": account["name"],
        "counter_account_code": template["counter_account"],
        "counter_account_name": counter["name"],
        "statement_section": account["statement"],
        "category": template["category"],
        "partner_name": partner,
        "cost_center": template["cost_center"],
        "payment_method": template["payment"],
        "quantity": quantity,
        "unit_price_net": f"{unit_price}",
        "amount_net": f"{amount_net}",
        "vat_rate": float(vat_rate),
        "vat_amount": f"{vat_amount}",
        "amount_gross": f"{amount_gross}",
        "currency": "EUR",
        "is_paid": paid,
        "is_recurring": recurring,
        "has_attachment": random.random() < 0.88,
        "is_credit_note": doc_type == "credit_note",
        "notes": maybe_missing(template["text"], 0.12),
    }


def main():
    year = 2025
    rows = [create_booking(i, year) for i in range(1, 301)]
    with open("output/buchungen_2025.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()