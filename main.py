import os
from google.oauth2 import service_account
from google.cloud import vision
import argparse
import cv2
import io
import re

credentials = "AIzaSyBMQDc912YtYmcaMSRyoprjmuhhXZVi23E"
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--client", required=True,
                help="key.json"
                     "n")
args = vars(ap.parse_args())

# create the client interface to access the Google Cloud Vision API
credentials = service_account.Credentials.from_service_account_file(
    filename=args["client"],
    scopes=["https://www.googleapis.com/auth/cloud-platform"])
client = vision.ImageAnnotatorClient(credentials=credentials)

file_name = os.path.abspath("1.jpg")

# Loads the image into memory
with open(file_name, "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.text_detection(image=image)
annotations = response.text_annotations

raw_data = ""

for annotation in annotations:
    raw_data = annotation.description
    print(raw_data)
    break


def extract_data(raw):
    global tankName
    result = []
    lines = raw.strip().split("\n")
    lines[lines.index("TANK 1") + 1], lines[lines.index("TANK 2") + 1], lines[lines.index("TANK 1")], lines[
        lines.index("TANK 2")] \
        = lines[lines.index("TANK 2") + 1], lines[lines.index("TANK 1") + 1], lines[lines.index("TANK 2")], lines[
        lines.index("TANK 1")]
    fuel_lvl = fuelFunc(lines)
    obj = {}
    i = 0
    while i < len(lines) - 2:

        line = lines[i]
        if line.startswith("TANK"):
            tankName = line
            tankVal = lines[i + 1]

            i += 1
            obj["tank_name"] = tankVal
            obj["fuel_Level"] = fuel_lvl.pop(0)
        elif line == "OIL LEVEL":
            oil_level = lines[i + 1]
            obj["oil_level"] = oil_level
        i += 1
        keyList = ["tank_name", "fuel_Level", "oil_level"]
        if all(elem in obj for elem in keyList):
            result.append({tankName: obj})
            obj = {}
    return result


def fuelFunc(data):
    fuelQueue = []
    for i in data:
        float_strings = re.search(re.compile(r"\d+\.\d+"), i)
        if (float_strings):
            fuelQueue.append(i)
    return fuelQueue


data = extract_data(raw_data)
print(data)
