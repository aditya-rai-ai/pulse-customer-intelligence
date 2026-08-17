def lookup_department(category: str) -> str:
    """Return the owning department and contact email for a customer-feedback category.
    Valid categories: Product Quality, Delivery, Pricing, Support, Freshness."""
    print(f"   [tool called → lookup_department(category='{category}')]")
    directory = {
        "product quality": "Product Management <product@company.com>",
        "delivery":        "Operations <ops@company.com>",
        "pricing":         "Finance <finance@company.com>",
        "support":         "Customer Support <support@company.com>",
        "freshness":       "Quality Assurance <qa@company.com>",
    }
    return directory.get(category.lower().strip(), "General Inquiries <hello@company.com>")