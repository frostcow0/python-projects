import requests
import polars as pl


def parse_int(val):
    if isinstance(val, str):
        val = val.replace(',', '').strip().lower()
        val = val.replace(' ', '').replace('+', '')
        if val.endswith('k'):
            return int(float(val[:-1]) * 1_000)
        elif val.endswith('m'):
            return int(float(val[:-1]) * 1_000_000)
        try:
            return int(val)
        except ValueError:
            return None
    elif isinstance(val, (int, float)):
        return int(val)
    return None

def main():
    details_url = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json"

    useful_keys = ["current"]
    herbs = [(3034, 3032), (2454, 2452), (121, 2428),
            (22464, 22461), (22452, 22449), (9741, 9739), (6472, 6470),
            (133, 2432), (24638, 24635), (24626, 24623), (23748, 23745),
            (23736, 23733), (23700, 23697), (23688, 23685), (23724, 23721),
            (23712, 23709)]
    results = {}

    for dose3, dose4 in herbs:
        dose3_data, dose4_data = None, None
        # dose3
        dose3_response = requests.get(details_url, params={"item":dose3})
        if dose3_response.status_code == 200:
            dose3_data = dose3_response.json()["item"]
            # print(dose3_data["name"])
        # dose4
        dose4_response = requests.get(details_url, params={"item":dose4})
        if dose4_response.status_code == 200:
            dose4_data = dose4_response.json()["item"]
        if not dose3_data or not dose4_data:
            print(f"Error with {dose3}:\n\t{dose3_response.status_code}\n\t{dose4_response.status_code}")
        else:
            results[dose3_data["name"]] = (
                [dose3_data[key] for key in dose3_data.keys() if key in useful_keys],
                [dose4_data[key] for key in dose4_data.keys() if key in useful_keys]
            )

    data = []
    for potion, (dose3_stats, dose4_stats) in results.items():
        row = {
            "potion": potion,
            "dose3_current": parse_int(dose3_stats[0]["price"]) if isinstance(dose3_stats[0], dict) and "price" in dose3_stats[0] else None,
            "dose4_current": parse_int(dose4_stats[0]["price"]) if isinstance(dose4_stats[0], dict) and "price" in dose4_stats[0] else None,
            "dose3_trend": dose3_stats[0]["trend"] if isinstance(dose3_stats[0], dict) and "trend" in dose3_stats[0] else None,
            "dose4_trend": dose4_stats[0]["trend"] if isinstance(dose4_stats[0], dict) and "trend" in dose4_stats[0] else None,
        }
        data.append(row)

    df = pl.DataFrame(data)

    df = df.with_columns([
        (df["dose4_current"] / 4).alias("dose4_per_dose_current"),
        (df["dose3_current"] / 3).alias("dose3_per_dose_current"),
    ])

    df = df.with_columns([
        (df["dose4_per_dose_current"] - df["dose3_per_dose_current"]).alias("per_dose_difference"),
    ])

    print(df.sort("per_dose_difference", descending=True).head())

if __name__ == '__main__':
    main()

