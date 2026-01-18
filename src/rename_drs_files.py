import os

# Directory containing your files
directory = "/home/cjw9009/Desktop/Senior_Project/DRSTamariskData/20250207/293.15/278.15-313.15_increment-5"

# Target name pattern length (e.g., "raw_192000" → 9 characters before extension)
target_length = len("raw_192000")

for filename in os.listdir(directory):
    old_path = os.path.join(directory, filename)

    # Skip directories
    if os.path.isdir(old_path):
        continue

    # Split name and extension
    name, ext = os.path.splitext(filename)

    if name.startswith("raw_"):
        number_part = name[4:]  # e.g., "2000"
        # Pad number to make the total name length match target_length
        padded_number = number_part.zfill(target_length - 4)
        new_name = f"raw_{padded_number}{ext}"
        new_path = os.path.join(directory, new_name)

        # Rename file
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")
