import requests
from bs4 import BeautifulSoup


def is_valid_potion(potion_name):
    # Filter out potions with square brackets in the name (e.g., "[upcoming]", "[Java Edition only]")
    if "[" in potion_name.lower():
        return False
    return True


def download_potion_data_to_file():
    url = "https://minecraft.fandom.com/wiki/Potion"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    potions = []

    # Save the raw HTML content to a file for reference
    with open("data/raw_potions.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
        print("Saved raw potion data to 'data/raw_potions.txt'")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the three specific tables using their class and data-description attributes
    positive_effect_table = soup.find('table', {'class': 'wikitable col-1-center', 'data-description': 'Positive potions'})
    negative_effect_table = soup.find('table', {'class': 'wikitable col-1-center', 'data-description': 'Negative potions'})
    base_potion_table = soup.find('table', {'class': 'wikitable col-1-center col-2-center', 'data-description': 'Base potions'})
    base_potion_table2 = soup.find('table', {'class': 'wikitable col-1-center col3-left', 'data-description': 'Base potions'})

    # Extract potion names from each table
    positive_potions = extract_potion_names(positive_effect_table)
    negative_potions = extract_potion_names(negative_effect_table)
    base_potions = extract_potion_names(base_potion_table)
    base_potions2 = extract_potion_names(base_potion_table2)  # The new Base potions table

    # Combine the potion lists from all four tables
    all_potions = positive_potions + negative_potions + base_potions + base_potions2

    # Add Lingering and Splash variants for each potion
    potions_with_variants = []
    for potion in all_potions:
        # Add the original potion name
        potions_with_variants.append(potion)
        # Add Lingering and Splash versions
        lingering_potion = "Lingering " + potion.strip()
        splash_potion = "Splash " + potion.strip()
        potions_with_variants.append(lingering_potion + "\n")
        potions_with_variants.append(splash_potion + "\n")
    tipped_arrows = []
    for potion in all_potions:
        tipped_arrows.append(potion.replace("Potion", "Arrow"))
    all_potion_items = potions_with_variants + tipped_arrows
    all_potion_items.sort()

    # Write the clean potion data (name, effects, Lingering, Splash) to a new file
    with open("data/clean_potions.txt", "w", encoding="utf-8") as f:
        f.writelines(all_potion_items)
        print("Saved clean potion data with variants to 'data/clean_potions.txt'")


def extract_potion_names(table):
    """Extract the potion name from each row of the given table (only header names)."""
    potions = []
    if table:
        rows = table.find_all('tr')[1:]  # Skip the header row

        for row in rows:
            th = row.find('th')  # Get the potion name from the header cell (<th>)
            if th:
                potion_name = th.get_text(strip=True)  # Potion name is in <th> element
                if is_valid_potion(potion_name):
                    potions.append(potion_name + "\n")

    return potions


# Run the function to download and process the potion data
download_potion_data_to_file()
