import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type, PhoneNumberType
from phonenumbers import PhoneNumberFormat as F

TYPES = {
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE: "Landline",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Landline or mobile",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.TOLL_FREE: "Toll-free",
}

def phoneinfomenu():
    raw = input("Enter phone number (with +): ").strip()

    try:
        num = phonenumbers.parse(raw, None)
        if not phonenumbers.is_valid_number(num):
            print("\nInvalid number")
        else:
            country = geocoder.country_name_for_number(num, "en")
            region = geocoder.description_for_number(num, "uk")

            print()
            print("International:", phonenumbers.format_number(num, F.INTERNATIONAL))
            print("National:", phonenumbers.format_number(num, F.NATIONAL))
            print("Country:", geocoder.description_for_number(num, "en") or "Unknown")

            if region and region != country:
                print("Region:", region)
            else:
                print("Region: not available (mobile numbers are not tied to a region)")

            print("Carrier:", carrier.name_for_number(num, "en") or "Unknown")
            print("Type:", TYPES.get(number_type(num), "Unknown"))
            print("Time zone:", ", ".join(timezone.time_zones_for_number(num)))

    except phonenumbers.NumberParseException:
        print("\nWrong format. Use +380...")

    input("\nPress Enter to continue...")

if __name__ == "__main__":
    phoneinfomenu()
