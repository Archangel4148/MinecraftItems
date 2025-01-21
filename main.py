from enchantment_data import download_enchantment_data_to_file
from item_data import download_item_data_to_file
from potion_data import download_potion_data_to_file

DOWNLOAD_DATA = True
UPDATE_COMBINED_DATA = True

if DOWNLOAD_DATA:
    # Update local files from online data
    download_item_data_to_file()
    download_enchantment_data_to_file()
    download_potion_data_to_file()

if UPDATE_COMBINED_DATA:
    # Read data from local files
    enchantments = open("data/clean_enchantments.txt", "r").readlines()
    items = open("data/clean_items.txt", "r").readlines()
    potions = open("data/clean_potions.txt", "r").readlines()

    # Combine item and enchantment data
    combined_list = enchantments + items + potions
    combined_list.sort()
    open("data/combined_list.txt", "w").writelines(combined_list)


all_items = open("data/combined_list.txt", "r").readlines()
print(len([name for name in all_items if "arrow of" in name.lower()]))
