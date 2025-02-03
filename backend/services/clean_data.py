import json

# Load the JSON file
with open("knowledge_base.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Remove duplicates (assuming data is a list of dictionaries)
original_count = len(data)
unique_data = list({json.dumps(item, sort_keys=True): item for item in data}.values())
new_count = len(unique_data)

# Overwrite the original file with cleaned data
with open("knowledge_base.json", "w", encoding="utf-8") as file:
    json.dump(unique_data, file, indent=4, ensure_ascii=False)

# Print the number of removed duplicates
duplicates_removed = original_count - new_count
print(f"Duplicates removed: {duplicates_removed}")
print("Updated data saved in 'knowledge_base.json'")
