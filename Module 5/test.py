def get_country_name(phone_number):
    """
    Returns the country name based on the phone number prefix.

    Format: '+XXOOOOOOOOOO'
    - '+34' -> Spain
    - '+66' -> Thailand (example native country)
    Raises:
        TypeError: if the phone number is not a string
        LookupError: if no country code found
        ValueError: if length or format is invalid
    """

    # 1️⃣ Type check
    if not isinstance(phone_number, str):
        raise TypeError("Phone number must be a string")

    # 2️⃣ Check format
    if not phone_number.startswith("+"):
        raise LookupError("Phone number must start with '+' and contain a country code")

    # 3️⃣ Basic length check
    if len(phone_number) < 4:  # must have at least +XX...
        raise ValueError("Phone number too short to contain a valid country code")

    # 4️⃣ Extract country code (up to 3 digits usually)
    country_code = phone_number[:3]  # e.g. +34, +66, +1
    full_length = len(phone_number)

    # 5️⃣ Validate total length
    if full_length != 13:
        raise ValueError("Phone number must contain country code + 10 digits (total length 13)")

    # 6️⃣ Map of known country codes
    country_codes = {
        "+34": "Spain",
        "+66": "Thailand",  # Example: your native country (you can change it)
        "+1": "United States / Canada",
        "+44": "United Kingdom",
        "+81": "Japan",
        "+49": "Germany",
    }

    # 7️⃣ Return country name or raise LookupError
    if country_code in country_codes:
        return country_codes[country_code]
    else:
        raise LookupError(f"Unknown country code: {country_code}")

# ✅ Example tests
try:
    print(get_country_name("+341234567890"))    # Spain
    print(get_country_name("+661234567890"))    # Thailand
    print(get_country_name("+34123abc7890"))    # Non-digit characters
except Exception as e:
    print(f"Error: {e}")

    # Uncomment each to see assertion failures:
    # print(get_country_name(12345))              # TypeError assertion
    # print(get_country_name("341234567890"))     # Missing '+'
    # print(get_country_name("+34123456"))        # Too short
    print(get_country_name("+991234567890"))    # Unknown code
