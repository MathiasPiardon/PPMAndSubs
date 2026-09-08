from datetime import datetime
from mrzmini import read_mrz
from pathlib import Path

def parse_passport(file_path: str) -> dict:
    """
    Extract information from the MRZ of a passport.

    Returns a dictionary suitable for insertion into PostgreSQL.
    """

    mrz = read_mrz(file_path)

    if mrz is None:
        raise ValueError("Could not detect an MRZ in the document.")

    data = mrz.to_dict()

    # Useful while developing:
    print("MRZ data:")
    print(data)

    # Make sure this really looks like a passport
    if data.get("mrz_type") != "TD3":
        raise ValueError(
            f"Expected a passport (TD3), got {data.get('mrz_type')}"
        )

    # Optional: require French passport
    if data.get("country") != "FRA":
        raise ValueError(
            f"Expected a French passport, got {data.get('country')}"
        )

    return {
        "first_name": data.get("names"),
        "last_name": data.get("surname"),
        "passport_number": data.get("number"),
        "nationality": data.get("nationality"),
        "date_of_birth": convert_mrz_date(data.get("date_of_birth")),
        "sex": data.get("sex"),
        "expiration_date": convert_mrz_date(data.get("expiration_date")),
    }


def convert_mrz_date(value):
    """
    Convert MRZ YYMMDD into a Python date.

    Example:
        850412 -> 1985-04-12
    """

    if not value:
        return None

    return datetime.strptime(value, "%y%m%d").date()

# test but call functions from MAin and # those ones
path = Path(r"G:\My Drive\PPMAndSubs\Investors\PassportMP.pdf")

data = parse_passport(str(path))

print(data)