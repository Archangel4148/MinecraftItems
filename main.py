from enchantment_data import download_enchantment_data_to_file
from item_data import download_item_data_to_file

DOWNLOAD_DATA = True

if DOWNLOAD_DATA:
    # Update local files from online data
    download_item_data_to_file()
    download_enchantment_data_to_file()

# Read data from local files
enchantments = open("data/clean_enchantments.txt", "r").readlines()
items = open("data/clean_items.txt", "r").readlines()

# Combine item and enchantment data
combined_list = enchantments + items
combined_list.sort()
open("data/combined_list.txt", "w").writelines(combined_list)
