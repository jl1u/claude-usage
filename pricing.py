"""
Shared pricing constants and helpers for cost estimation.
"""

PRICING = {
    "claude-opus-4-6":   {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "claude-opus-4-5":   {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "claude-opus-4-1":   {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "claude-opus-4":     {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "claude-sonnet-4-6": {"input":  3.00, "output": 15.00, "cache_write":  3.75, "cache_read": 0.30},
    "claude-sonnet-4-5": {"input":  3.00, "output": 15.00, "cache_write":  3.75, "cache_read": 0.30},
    "claude-sonnet-4":   {"input":  3.00, "output": 15.00, "cache_write":  3.75, "cache_read": 0.30},
    "claude-haiku-4-6":  {"input":  1.00, "output":  5.00, "cache_write":  1.25, "cache_read": 0.10},
    "claude-haiku-4-5":  {"input":  1.00, "output":  5.00, "cache_write":  1.25, "cache_read": 0.10},
}


def is_billable_model(model):
    if not model:
        return False
    model_lower = model.lower()
    return "opus" in model_lower or "sonnet" in model_lower or "haiku" in model_lower


def get_pricing(model):
    if not model:
        return None
    if model in PRICING:
        return PRICING[model]
    for key, value in PRICING.items():
        if model.startswith(key):
            return value

    model_lower = model.lower()
    if "opus" in model_lower:
        return PRICING["claude-opus-4-6"]
    if "sonnet" in model_lower:
        return PRICING["claude-sonnet-4-6"]
    if "haiku" in model_lower:
        return PRICING["claude-haiku-4-5"]
    return None


def calc_cost(model, inp, out, cache_read, cache_creation):
    pricing = get_pricing(model)
    if not pricing:
        return 0.0
    return (
        inp * pricing["input"] / 1_000_000 +
        out * pricing["output"] / 1_000_000 +
        cache_read * pricing["cache_read"] / 1_000_000 +
        cache_creation * pricing["cache_write"] / 1_000_000
    )
