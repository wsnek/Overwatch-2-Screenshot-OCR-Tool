
import cv2
import pytesseract
import csv
import os
import re

#This is something that can be played around with (PLEASE ONLY EDIT THIS IF YOU KNOW WHAT YOU ARE DOING AND HAVE READ UP ON THIS)
PyTessConfig = "--oem 1 --psm 6 -c tessedit_char_whitelist=0123456789"
'''
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
       bypassing hacks that are Tesseract-specific.
'''
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  # your path may be different

# Define the directory where the screenshots are located
os.chdir("data")
screenshot_dir = "./"

# Define the fixed positions for attribute extraction
# Format follows: "Attribute Name": (Position X, Position Y), (Crop Height, Crop Width)
attribute_positions = {
    "Tank_Eliminations_Team": ((700, 210), (25, 31)),
    "Tank_Assists_Team": ((750, 210), (25, 31)),
    "Tank_Deaths_Team": ((800, 210), (25, 31)),
    "Tank_Damage_Team": ((860, 210), (34, 100)),
    "Tank_Healing_Team": ((965, 210), (34, 100)),
    "Tank_Mitigation_Team": ((1065, 210), (34, 100)),

    "DPS1_Eliminations_Team": ((700, 270), (25, 31)),
    "DPS1_Assists_Team": ((750, 270), (25, 31)),
    "DPS1_Deaths_Team": ((800, 270), (25, 31)),
    "DPS1_Damage_Team": ((860, 270), (34, 100)),
    "DPS1_Healing_Team": ((965, 270), (34, 100)),
    "DPS1_Mitigation_Team": ((1065, 270), (34, 100)),

    "DPS2_Eliminations_Team": ((700, 330), (25, 31)),
    "DPS2_Assists_Team": ((750, 330), (25, 31)),
    "DPS2_Deaths_Team": ((800, 330), (25, 31)),
    "DPS2_Damage_Team": ((860, 330), (34, 100)),
    "DPS2_Healing_Team": ((965, 330), (34, 100)),
    "DPS2_Mitigation_Team": ((1065, 330), (34, 100)),

    "Support1_Eliminations_Team": ((700, 390), (25, 31)),
    "Support1_Assists_Team": ((750, 390), (25, 31)),
    "Support1_Deaths_Team": ((800, 390), (25, 31)),
    "Support1_Damage_Team": ((860, 390), (34, 100)),
    "Support1_Healing_Team": ((965, 390), (34, 100)),
    "Support1_Mitigation_Team": ((1065, 390), (34, 100)),

    "Support2_Eliminations_Team": ((700, 450), (25, 31)),
    "Support2_Assists_Team": ((750, 450), (25, 31)),
    "Support2_Deaths_Team": ((800, 450), (25, 31)),
    "Support2_Damage_Team": ((860, 450), (34, 100)),
    "Support2_Healing_Team": ((965, 450), (34, 100)),
    "Support2_Mitigation_Team": ((1065, 450), (34, 100)),


    "Tank_Eliminations_Enemy": ((700, 630),(25, 31)),
    "Tank_Assists_Enemy": ((750, 630),(25, 31)),
    "Tank_Deaths_Enemy": ((800, 630),(25, 31)),
    "Tank_damage_Enemy": ((860, 630), (34, 100)),
    "Tank_healing_Enemy": ((965, 630), (34, 100)),
    "Tank_mitigation_Enemy": ((1065, 630), (34, 100)),

    "DPS1_Eliminations_Enemy": ((700, 690),(25, 31)),
    "DPS1_Assists_Enemy": ((750, 690),(25, 31)),
    "DPS1_Deaths_Enemy": ((800, 690),(25, 31)),
    "DPS1_damage_Enemy": ((860, 690),(34, 100)),
    "DPS1_healing_Enemy": ((965, 690),(34, 100)),
    "DPS1_mitigation_Enemy": ((1065, 690), (34, 100)),

    "DPS2_Eliminations_Enemy": ((700, 750),(25, 31)),
    "DPS2_Assists_Enemy": ((750, 750),(25, 31)),
    "DPS2_Deaths_Enemy": ((800, 750),(25, 31)),
    "DPS2_damage_Enemy": ((860, 750), (34, 100)),
    "DPS2_healing_Enemy": ((965, 750), (34, 100)),
    "DPS2_mitigation_Enemy": ((1065, 750), (34, 100)),

    "Support1_Eliminations_Enemy": ((700, 810),(25, 31)),
    "Support1_Assists_Enemy": ((750, 810),(25, 31)),
    "Support1_Deaths_Enemy": ((800, 810),(25, 31)),
    "Support1_damage_Enemy": ((860, 810), (34, 100)),
    "Support1_healing_Enemy": ((965, 810), (34, 100)),
    "Support1_mitigation_Enemy": ((1065, 810), (34, 100)),

    "Support2_Eliminations_Enemy": ((700, 870),(25, 31)),
    "Support2_Assists_Enemy": ((750, 870),(25, 31)),
    "Support2_Deaths_Enemy": ((800, 870),(25, 31)),
    "Support2_damage_Enemy": ((860, 870), (34, 100)),
    "Support2_healing_Enemy": ((965, 870), (34, 100)),
    "Support2_mitigation_Enemy": ((1065, 870), (34, 100)),

}

# Get a list of the screenshot and sort them NATURALLY
screenshot_files = os.listdir(screenshot_dir)
screenshot_files = sorted(screenshot_files, key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)])

# Initialize the results list
results = []

# Get the list of already processed image names from the CSV file
processed_images = set()
output_file = "result.csv"
if os.path.isfile(output_file):
    with open(output_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        if "Image" in reader.fieldnames:
            for row in reader:
                if "Image" in row:
                    processed_images.add(row["Image"])


# Iterate over the screenshots in the directory
i = 0
for screenshot_file in screenshot_files:
    if not screenshot_file.endswith(".bmp"):
        continue
    
    screenshot_path = os.path.join(screenshot_dir, screenshot_file)

    # Check if the image has already been processed
    if screenshot_file in processed_images:
        print(f"Skipping file: {screenshot_path} (already processed)")
        continue

    print(f"Processing file: {screenshot_path}")

    # Load the image
    image = cv2.imread(screenshot_path)

    # Split the input image into its RGB channels
    b, g, r = cv2.split(image)

    # Convert to grayscale using the minimum channel for each pixel
    gray_image = cv2.min(b, cv2.min(g, r))

    # Apply Gaussian blur to reduce noise in the image
    denoised_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced_image = clahe.apply(denoised_image)
    
    # DEBUG: Save this image to the disk
    if i == 0: cv2.imwrite("CONTR" + screenshot_file, contrast_enhanced_image)

    # Extract the attribute values using pytesseract
    attributes = {"Image": screenshot_file}  # Add image name as the first attribute

    text = pytesseract.image_to_string(contrast_enhanced_image, config=PyTessConfig)

    for attribute, (position, crop_size) in attribute_positions.items():
        x, y = position
        crop = contrast_enhanced_image[y:y + crop_size[0], x:x + crop_size[1]]
        if i == 0: cv2.imwrite("CROP_" + attribute + "_" + screenshot_file, crop)
        result = pytesseract.image_to_string(crop, config="--psm 7")
        attributes[attribute] = result.strip()

    # Append the attributes to the results list
    results.append(attributes)
    i+=1

# Write the results to the CSV file
with open(output_file, "a", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(attribute_positions.keys()) + ["Image"])
    if not processed_images:
        writer.writeheader()
    writer.writerows(results)

print(f"Results saved to: {output_file}")
