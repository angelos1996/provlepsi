# utils.py

def parse_float(val: str) -> float:
    if not val:
        return 0.0
    return float(val.replace(",", ".").strip())

def euro(amount: float) -> str:
    return f"{amount:,.2f} €"
