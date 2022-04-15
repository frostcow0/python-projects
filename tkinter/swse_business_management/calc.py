def calc(drug, quantity) -> float:
    quality = {
        "GLITTERSTIM": "common",
        "DEATHSTICKS": "common",
        "NYRIANN SPICE": "exotic",
        "TEMPEST": "exotic",
        "THISTLEBARK": "exotic",
    }

    price = {
        "common": 1000,
        "exotic": 20000,
    }

    return quantity * price[quality[drug]]

inventory = [["GLITTERSTIM", 125], ["DEATHSTICKS", 500],
    ["NYRIANN SPICE", 125], ["TEMPEST", 125],
    ["THISTLEBARK", 125]]

total = 0
for item in inventory:
    total += calc(item[0], item[1])

print(total)
