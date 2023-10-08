
import cv2
import pytesseract
import csv
import os
import re





#This is something that can be played around with (PLEASE ONLY EDIT THIS IF YOU KNOW WHAT YOU ARE DOING AND HAVE READ UP ON THIS)
PyTessConfig = "--oem 1 --psm 6 -c tessedit_char_whitelist=0123456789"

class ImagePreprocessor:
    def __init__(self):
        pass

    def resize_image(self, image, width=None, height=None):
        """
        Resize the image to the specified width and/or height while maintaining aspect ratio.
        """
        if width is None and height is None:
            return image

        if width is None:
            aspect_ratio = height / float(image.shape[0])
            new_width = int(image.shape[1] * aspect_ratio)
            new_height = height
        elif height is None:
            aspect_ratio = width / float(image.shape[1])
            new_width = width
            new_height = int(image.shape[0] * aspect_ratio)
        else:
            new_width = width
            new_height = height

        resized_image = cv2.resize(image, (new_width, new_height))
        return resized_image

    def denoise_image(self, image, kernel_size=5):
        """
        Apply Gaussian blur to reduce noise in the image.
        """
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def enhance_contrast(self, image):
        """
        Enhance the contrast of the image.
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(gray_image)

    def preprocess(self, image, resize_width=None, resize_height=None):
        """
        Preprocess the image using a series of steps.
        """
        # Resize the image
        resized_image = self.resize_image(image, width=resize_width, height=resize_height)

        # Denoise the image
        denoised_image = self.denoise_image(resized_image)

        # Enhance contrast
        contrast_enhanced_image = self.enhance_contrast(denoised_image)

        return contrast_enhanced_image


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

# Define the directory where the screenshots are located
screenshot_dir = "./"

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
for screenshot_file in screenshot_files:
    if screenshot_file.endswith(".bmp"):
        screenshot_path = os.path.join(screenshot_dir, screenshot_file)

        # Check if the image has already been processed
        if screenshot_file in processed_images:
            print(f"Skipping file: {screenshot_path} (already processed)")
            continue

        print(f"Processing file: {screenshot_path}")


        preprocessor = ImagePreprocessor()

        # Load the image
        image = cv2.imread(screenshot_path)



        preprocessed_image = preprocessor.preprocess(image, resize_width=600, resize_height=None)
        text = pytesseract.image_to_string(preprocessed_image, config=PyTessConfig)

        # Extract the attribute values using pytesseract
        attributes = {"Image": screenshot_file}  # Add image name as the first attribute
        for attribute, (position, crop_size) in attribute_positions.items():
            x, y = position
            crop = image[y:y + crop_size[0], x:x + crop_size[1]]
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, crop = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            result = pytesseract.image_to_string(crop, config="--psm 7")
            attributes[attribute] = result.strip()

        # Append the attributes to the results list
        results.append(attributes)

# Write the results to the CSV file
with open(output_file, "a", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(attribute_positions.keys()) + ["Image"])
    if not processed_images:
        writer.writeheader()
    writer.writerows(results)

print(f"Results saved to: {output_file}")

