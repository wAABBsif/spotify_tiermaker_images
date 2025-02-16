Spotify TierMaker Images
====
This Python script generates image templates of songs for use with TierMaker, with a format of white text on top of a darkened album cover. Using [SpotAPI](https://github.com/Aran404/SpotAPI), it includes support for albums and playlists from Spotify to generate multiple images of songs, along with custom album covers.

Instructions
--------
1. Install dependencies
```
pip install -r requirements.txt
```
2. Run ``stmi.py`` with template parammeters in a ``.json`` file as an argument
```
python stmi.py example.json
```
Template Parameters
--------
**See ``example.json`` for reference**
- ``font`` (optional, string): File name of font to be used on images
- ``fontSize`` (optional, number): Size of font to be used on images
- ``lineSize`` (optional, number): Maximum amount of characters on one line of text on images
- ``entries`` (required, array): List of entries of songs, albums, or playlists in order to create images
  - - ``type`` (required, string): Either ``song``, ``album``, or ``playlist``
  - **``song``**
    - ``name`` (required, string): Name of song
    - ``cover`` (required, string): URI to background image to use for song
  - **``album``**
    - ``uri`` (required, string): Spotify URI of album
    - ``cover`` (optional, string): URI to image replacement for album cover
    - ``discs`` (optional, array): List of discs to create images of songs from
    - ``maxCount`` (optional, number): Maximum amount of songs to create images from
  - **``playlist``**
    - ``uri`` (required, string): Spotify URI of playlist
    - ``cover`` (optional, string): URI to image replacement for album covers
    - ``maxCount`` (optional, number): Maximum amount of songs to create images from
