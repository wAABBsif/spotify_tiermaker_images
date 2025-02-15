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
    img = img.resize((512, 512))
    img = Image.eval(img, lambda color: 128 + color/2)

    i_draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(font_size)
    if font_name != "":
        font = ImageFont.truetype(font_name, font_size)
    _, _, w, h = i_draw.multiline_textbbox((0, 0), text=finalText, font=font, align="center")
    i_draw.multiline_text(((img.width - w) / 2, (img.height - h) / 2), finalText, (0, 0, 0), font=font, align="center")

    pathlib.Path("images").mkdir(parents=True, exist_ok=True) 
    img.save("images/" + str(image_count) + ".png")

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
    info = album.get_album_info()
    print("Loading album \"" + info["data"]["albumUnion"]["name"] + "\"")
    count = 0
    coverArtLink = info["data"]["albumUnion"]["coverArt"]["sources"][0]["url"]
    for t_entry in info["data"]["albumUnion"]["tracksV2"]["items"]:
        if "maxCount" in entry:
            if count >= entry["maxCount"]:
                break
        disc_no = t_entry["track"]["discNumber"]
        if "discs" in entry:
            if disc_no not in entry["discs"]:
                continue
        name = t_entry["track"]["name"]
        create_and_save_image(name, entry.get("cover", coverArtLink), font, font_size, line_size)
        count += 1

def handle_playlist(entry):
    global font
    global font_size
    global line_size
    playlist = PublicPlaylist(entry["uri"])
    info = playlist.get_playlist_info()
    print("Loading playlist \"" + info["data"]["playlistV2"]["name"] + "\"")
    count = 0
    for t_entry in info["data"]["playlistV2"]["content"]["items"]:
        if "maxCount" in entry:
            if count >= entry["maxCount"]:
                break
        coverArtLink = t_entry["itemV2"]["data"]["albumOfTrack"]["coverArt"]["sources"][0]["url"]
        name = t_entry["itemV2"]["data"]["name"]
        create_and_save_image(name, entry.get("cover", coverArtLink), font, font_size, line_size)
        count += 1

file = open("example.json", "r")
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