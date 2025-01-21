import re

import requests

INVALID_ITEMS = ["bartering", "enchanted book", "air", "potion"]


def is_valid_item(item_name: str, invalid_items: list[str]):
    for invalid_item in invalid_items:
        if invalid_item == "air" and "Air" not in item_name:
            return True
        if invalid_item in item_name.lower():
            return False
    return True


def clean_raw_item_text(text: str):
    return text.replace("net.minecraft.world.item.Item ", "").replace("_", " ").title()


def download_item_data_to_file():
    url = "https://piston-data.mojang.com/v1/objects/0530a206839eb1e9b35ec86acbbe394b07a2d9fb/client.txt"
    pattern = r"^net\.minecraft\.world\.item\.Item\s([A-Z_]+)\s->\s([a-zA-Z]+)$"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the file. Status code: {response.status_code}")
        return

    items = []

    with open("data/raw_items.txt", "w") as f:
        f.write(response.text)
        print("Saved raw item data to \'data/raw_items.txt\'")

    with open("data/clean_items.txt", "w") as f:
        for line in response.text.split("\n"):
            stripped_line = line.strip()  # Strip leading/trailing whitespace once
            if stripped_line.startswith("net.minecraft.world.item.Item "):

                if re.match(pattern, line.strip()):
                    item_name = clean_raw_item_text(stripped_line.split(" -> ")[0])
                    if not is_valid_item(item_name, INVALID_ITEMS):
                        continue
                    items.append(item_name)
                    if "pottery" in item_name.lower():
                        items.append(item_name.replace(" Pottery Sherd", " Decorated Pot"))

        # Sort the items alphabetically
        items.sort()

        # Write the sorted items to the file
        f.write("\n".join(items) + "\n")
        print("Saved parsed items to \'data/clean_items.txt\'")
