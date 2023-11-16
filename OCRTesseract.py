
import cv2
import pytesseract
import csv
import os
import re

#This is something that can be played around with (PLEASE ONLY EDIT THIS IF YOU KNOW WHAT YOU ARE DOING AND HAVE READ UP ON THIS)
PyTessConfig = "--oem 1 --psm 7 -c tessedit_char_whitelist=0123456789, tessedit_char_whitelist=\"qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM\""
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
    "Tank_Eliminations_Team": ((700, 210), (30, 35)),
    "Tank_Assists_Team": ((750, 210), (30, 35)),
    "Tank_Deaths_Team": ((805, 210), (30, 35)),
    "Tank_Damage_Team": ((860, 210), (34, 100)),
    "Tank_Healing_Team": ((965, 210), (34, 100)),
    "Tank_Mitigation_Team": ((1065, 210), (34, 100)),

    "DPS1_Eliminations_Team": ((700, 273), (30, 35)),
    "DPS1_Assists_Team": ((750, 273), (30, 35)),
    "DPS1_Deaths_Team": ((805, 273), (30, 35)),
    "DPS1_Damage_Team": ((860, 273), (34, 100)),
    "DPS1_Healing_Team": ((965, 273), (34, 100)),
    "DPS1_Mitigation_Team": ((1065, 273), (34, 100)),

    "DPS2_Eliminations_Team": ((700, 336), (30, 35)),
    "DPS2_Assists_Team": ((750, 336), (30, 35)),
    "DPS2_Deaths_Team": ((805, 336), (30, 35)),
    "DPS2_Damage_Team": ((860, 336), (34, 100)),
    "DPS2_Healing_Team": ((965, 336), (34, 100)),
    "DPS2_Mitigation_Team": ((1065, 336), (34, 100)),

    "Support1_Eliminations_Team": ((700, 399), (30, 35)),
    "Support1_Assists_Team": ((750, 399), (30, 35)),
    "Support1_Deaths_Team": ((805, 399), (30, 35)),
    "Support1_Damage_Team": ((860, 399), (34, 100)),
    "Support1_Healing_Team": ((965, 399), (34, 100)),
    "Support1_Mitigation_Team": ((1065, 399), (34, 100)),

    "Support2_Eliminations_Team": ((700, 462), (30, 35)),
    "Support2_Assists_Team": ((750, 462), (30, 35)),
    "Support2_Deaths_Team": ((805, 462), (30, 35)),
    "Support2_Damage_Team": ((860, 462), (34, 100)),
    "Support2_Healing_Team": ((965, 462), (34, 100)),
    "Support2_Mitigation_Team": ((1065, 462), (34, 100)),


    "Tank_Eliminations_Enemy": ((700, 630),(30, 35)),
    "Tank_Assists_Enemy": ((750, 630),(30, 35)),
    "Tank_Deaths_Enemy": ((805, 630),(30, 35)),
    "Tank_damage_Enemy": ((860, 630), (34, 100)),
    "Tank_healing_Enemy": ((965, 630), (34, 100)),
    "Tank_mitigation_Enemy": ((1065, 630), (34, 100)),

    "DPS1_Eliminations_Enemy": ((700, 691),(30, 35)),
    "DPS1_Assists_Enemy": ((750, 691),(30, 35)),
    "DPS1_Deaths_Enemy": ((805, 691),(30, 35)),
    "DPS1_damage_Enemy": ((860, 691),(34, 100)),
    "DPS1_healing_Enemy": ((965, 691),(34, 100)),
    "DPS1_mitigation_Enemy": ((1065, 691), (34, 100)),

    "DPS2_Eliminations_Enemy": ((700, 752),(30, 35)),
    "DPS2_Assists_Enemy": ((750, 752),(30, 35)),
    "DPS2_Deaths_Enemy": ((805, 752),(30, 35)),
    "DPS2_damage_Enemy": ((860, 752), (34, 100)),
    "DPS2_healing_Enemy": ((965, 752), (34, 100)),
    "DPS2_mitigation_Enemy": ((1065, 752), (34, 100)),

    "Support1_Eliminations_Enemy": ((700, 813),(30, 35)),
    "Support1_Assists_Enemy": ((750, 813),(30, 35)),
    "Support1_Deaths_Enemy": ((805, 813),(30, 35)),
    "Support1_damage_Enemy": ((860, 813), (34, 100)),
    "Support1_healing_Enemy": ((965, 813), (34, 100)),
    "Support1_mitigation_Enemy": ((1065, 813), (34, 100)),

    "Support2_Eliminations_Enemy": ((700, 874),(30, 35)),
    "Support2_Assists_Enemy": ((750, 874),(30, 35)),
    "Support2_Deaths_Enemy": ((805, 874),(30, 35)),
    "Support2_damage_Enemy": ((860, 874), (34, 100)),
    "Support2_healing_Enemy": ((965, 874), (34, 100)),
    "Support2_mitigation_Enemy": ((1065, 874), (34, 100)),

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
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    #contrast_enhanced_image = clahe.apply(denoised_image)
    
    # DEBUG: Save this image to the disk
    '''
    if i == 0:
        cv2.imwrite("CONTR0" + screenshot_file, denoised_image)
        cv2.imwrite("CONTR1" + screenshot_file, contrast_enhanced_image)
        cv2.imwrite("CONTR2" + screenshot_file, contrast_enhanced_image2)
        cv2.imwrite("CONTR3" + screenshot_file, contrast_enhanced_image3)
        cv2.imwrite("CONTR4" + screenshot_file, contrast_enhanced_image4)
    '''

    # Extract the attribute values using pytesseract
    attributes = {"Image": screenshot_file}  # Add image name as the first attribute

    #text = pytesseract.image_to_string(contrast_enhanced_image, config=PyTessConfig)

    for attribute, (position, crop_size) in attribute_positions.items():
        x, y = position
        crop = denoised_image[y:y + crop_size[0], x:x + crop_size[1]]
        if i == 0: cv2.imwrite("Crop_" + attribute + "_" + screenshot_file, crop)
        result = pytesseract.image_to_string(crop, config=PyTessConfig)
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
