def validate_required_fields(data, required_fields):
    """Utility to validate that all required fields are present in data."""
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"'{field}' is required"
    return True, None
