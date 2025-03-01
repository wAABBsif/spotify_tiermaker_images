import math
import sys
import textwrap
from spotapi import PublicAlbum, PublicPlaylist
from PIL import Image, ImageDraw, ImageFont
import json
import requests
import pathlib

image_count = 0
def create_and_save_image(trackName, imageUri, font_name, font_size, line_size):
    global image_count
    image_count = image_count + 1
    print("Saving image for " + trackName)

    lines = textwrap.wrap(trackName, width=line_size)
    finalText = ""
    for line in lines:
        finalText += line + "\n"

    img = Image.open(requests.get(imageUri, stream=True).raw)
    img = img.convert("RGB")
    img = img.resize((400, 400))
    img = Image.eval(img, lambda color: color/2)

    i_draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(font_size)
    if font_name != "":
        font = ImageFont.truetype(font_name, font_size)
    _, _, w, h = i_draw.multiline_textbbox((0, 0), text=finalText, font=font, align="center")
    i_draw.multiline_text(((img.width - w) / 2, (img.height - h) / 2), finalText, (255, 255, 255), font=font, align="center")

    folderName = sys.argv[1]
    folderName = folderName[0:len(folderName) - 5]
    pathlib.Path(folderName).mkdir(parents=True, exist_ok=True) 
    img.save(folderName + "/" + str(image_count).zfill(4) + ".jpg", optimize=True, quality=85)

def handle_song(entry):
    global font
    global font_size
    global line_size
    create_and_save_image(entry["name"], entry["cover"], font, font_size, line_size)

def handle_album(entry):
    global font
    global font_size
    global line_size
    album = PublicAlbum(entry["uri"])
    info = album.get_album_info(entry.get("maxCount", 1024))
    print("Loading album \"" + info["data"]["albumUnion"]["name"] + "\"")
    coverArtLink = info["data"]["albumUnion"]["coverArt"]["sources"][0]["url"]
    for t_entry in info["data"]["albumUnion"]["tracksV2"]["items"]:
        disc_no = t_entry["track"]["discNumber"]
        if "discs" in entry:
            if disc_no not in entry["discs"]:
                continue
        name = t_entry["track"]["name"]
        create_and_save_image(name, entry.get("cover", coverArtLink), font, font_size, line_size)

def handle_playlist(entry):
    global font
    global font_size
    global line_size
    playlist = PublicPlaylist(entry["uri"])
    info = playlist.get_playlist_info(entry.get("maxCount", 1024))
    print("Loading playlist \"" + info["data"]["playlistV2"]["name"] + "\"")
    for t_entry in info["data"]["playlistV2"]["content"]["items"]:
        coverArtLink = t_entry["itemV2"]["data"]["albumOfTrack"]["coverArt"]["sources"][0]["url"]
        name = t_entry["itemV2"]["data"]["name"]
        create_and_save_image(name, entry.get("cover", coverArtLink), font, font_size, line_size)

if len(sys.argv) < 2:
	raise Exception("No file parameter passed")

file = open(sys.argv[1], "r")
file_data = json.load(file)

font = file_data.get("font", "")
font_size = file_data.get("fontSize", 48)
line_size = file_data.get("lineSize", 12)

for entry in file_data["entries"]:
    match entry["type"]:
        case "song":
            handle_song(entry)
        case "album":
            handle_album(entry)
        case "playlist":
            handle_playlist(entry)