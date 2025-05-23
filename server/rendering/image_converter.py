
import os
import time
from PIL import Image
from io import BytesIO
import logging

from enum import Enum

class Palette(Enum):
    BW = (
        [0, 0, 0],          # Schwarz
        [255, 255, 255]     # Weiß
    )
    BWR = (
        [0, 0, 0],          # Schwarz
        [255, 255, 255],    # Weiß
        [255, 0, 0]         # Rot
    )
    BWY = (
        [0, 0, 0],          # Schwarz
        [255, 255, 255],    # Weiß
        [255, 255, 0]       # Gelb
    )
    BWRY = (
        [0, 0, 0],          # Schwarz
        [255, 255, 255],    # Weiß
        [255, 0, 0],        # Rot
        [255, 255, 0]       # Gelb
    )
    RGB = (
        [0, 0, 0],          # Schwarz
        [255, 255, 255],    # Weiß
        [255, 255, 0],      # Gelb
        [255, 0, 0],        # Rot
        [0, 0, 255],        # Blau
        [0, 255, 0]         # Grün
    )

class ImageConverter:
    
    def convert(self, img: Image, palette: Palette) -> Image:
        start_time = time.time()
        
        # Farbpalette abrufen
        palette_flat = sum(palette.value, [])  # flatten list of lists
        # Palette muss 768 Werte (256*3) haben
        palette_flat += [0] * (768 - len(palette_flat))
        
        # In P-Modus mit Floyd-Steinberg Dithering konvertieren
        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette(palette_flat)
        result = img.convert("RGB").quantize(palette=pal_img, dither=Image.FLOYDSTEINBERG)
        
        process_time = time.time() - start_time
        print(f"Bildverarbeitung abgeschlossen in {process_time:.2f}s")
        
        return result