import re

import requests
from bs4 import BeautifulSoup


def to_roman(num):
    roman_numerals = {
        1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    return roman_numerals.get(num, str(num))


def is_valid_enchantment(enchantment_name):
    if "upcoming" in enchantment_name.lower():
        return False
    return True


def clean_enchantment_name(enchantment_name):
    # Remove anything inside square brackets, e.g., "[upcoming]" or "[Java Edition only]"
    enchantment_name = re.sub(r'\[.*?\]', '', enchantment_name).strip()

    # Further cleanup: Remove any trailing spaces or non-alphabetic characters if needed
    enchantment_name = re.sub(r'[^A-Za-z0-9 ]', '', enchantment_name).strip()

    return enchantment_name


def download_enchantment_data_to_file():
    url = "https://minecraft.fandom.com/wiki/Enchanting"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    enchantments = []

    with open("data/raw_enchantments.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
        print("Saved raw enchantment data to \'data/raw_enchantments.txt\'")


    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Open the file to write the enchantment data using UTF-8 encoding
    with open("data/clean_enchantments.txt", "w", encoding="utf-8") as f:
        # Find the table with the specific class
        table = soup.find('table', {'class': 'wikitable sortable col-1-left col-2-left'})

        if not table:
            print("Table not found!")
            return  # Exit if the table is not found

        # Find all rows in the table (ignoring the header row)
        rows = table.find_all('tr')[1:]

        for row in rows:
            # Extract the columns (td elements) from the row
            columns = row.find_all('td')

            if len(columns) >= 5:  # Ensure that the row has at least five columns (name and max level)
                enchantment_name = columns[0].get_text(strip=True)
                max_level_text = columns[4].get_text(strip=True)

                if not is_valid_enchantment(enchantment_name):
                    continue

                # Clean the enchantment name (remove unwanted text like Java Edition only, upcoming, etc.)
                enchantment_name = clean_enchantment_name(enchantment_name)

                # Clean the max_level_text and extract the numerical part
                cleaned_max_level = re.sub(r"[^\d]", "", max_level_text)  # Keep only digits

                if cleaned_max_level.isdigit():
                    max_enchantment_level = int(cleaned_max_level)  # Convert to integer
                else:
                    max_enchantment_level = 0  # If it can't be cleaned, set to 0

                # Generate all possible enchantment levels using Roman numerals
                for level in range(1, max_enchantment_level + 1):
                    roman_level = to_roman(level)
                    enchantments.append(f"{enchantment_name} {roman_level}")

        # Sort the enchantments alphabetically
        enchantments.sort()

        # Write the sorted enchantments to the file
        f.write("\n".join(enchantments) + "\n")
        print("Saved parsed enchantments to \'data/clean_enchantments.txt\'")

