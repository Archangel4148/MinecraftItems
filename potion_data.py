import requests
from bs4 import BeautifulSoup


def is_valid_potion(potion_name):
    if "[" in potion_name.lower():
        return False
    return True


def download_potion_data_to_file():
    url = "https://minecraft.fandom.com/wiki/Potion"

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    potions = []

    # Save the raw HTML content to a file
    with open("data/raw_potions.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
        print("Saved raw potion data to 'data/raw_potions.txt'")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the two specific tables using their class and data-description
    positive_effect_table = soup.find('table',
                                      {'class': 'wikitable col-1-center', 'data-description': 'Positive potions'})
    negative_effect_table = soup.find('table',
                                      {'class': 'wikitable col-1-center', 'data-description': 'Negative potions'})

    # Extract the relevant columns (1st, 3rd, and 4th columns) from both tables
    positive_potions = extract_potion_names(positive_effect_table)
    negative_potions = extract_potion_names(negative_effect_table)

    # Combine both lists
    all_potions = positive_potions + negative_potions

    # Write the potion data (name, extended effect, enhanced duration) to a new file
    with open("data/clean_potions.txt", "w", encoding="utf-8") as f:
        f.writelines(all_potions)
        print("Saved clean potion data to 'data/clean_potions.txt'")


def extract_potion_names(table):
    """Extract the potion name, duration, and effects from each row of the given table."""
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
