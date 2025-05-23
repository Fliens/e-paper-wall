# run with python -m server.rendering.example_layouts.create

from PIL import Image, ImageDraw
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from server.rendering.content_renderer import ContentRenderer

def make_dummy_image(mode, size, color):
    img = Image.new(mode, size, color)
    draw = ImageDraw.Draw(img)
    return img

def all_param_combinations():
    # Reihenfolge: title, subtitle, url, image (image immer dabei)
    title = "Beispiel Titel"
    subtitle = "Beispiel Untertitel"
    url = "https://example.com"
    # Alle Kombinationen außer image weglassen
    combos = [
        {"title": title, "subtitle": subtitle, "url": url},
        {"title": title, "subtitle": subtitle, "url": None},
        {"title": title, "subtitle": None, "url": None},
        {"title": None, "subtitle": None, "url": None},
    ]
    return combos

def main():
    outdir = "server/rendering/example_layouts"
    os.makedirs(outdir, exist_ok=True)
    # Display- und Bildformate
    layouts = [
        ("horizontal_landscape", (800, 480), (800, 480)),
        ("horizontal_portrait", (800, 480), (400, 600)),
        ("vertical_landscape", (480, 800), (800, 480)),
        ("vertical_portrait", (480, 800), (400, 600)),
    ]
    for layout_name, disp_res, img_res in layouts:
        for params in all_param_combinations():
            # Dummy-Bild erzeugen
            img = make_dummy_image("RGB", img_res, "#cccccc")
            renderer = ContentRenderer(
                resolution=disp_res,
                image=img,
                title=params["title"],
                subtitle=params["subtitle"],
                url=params["url"]
            )
            result = renderer.render()
            # Dateinamen bauen
            parts = [layout_name]
            if params["title"]: parts.append("title")
            if params["subtitle"]: parts.append("subtitle")
            if params["url"]: parts.append("url")
            parts.append("image")
            fname = "_".join(parts) + ".png"
            fpath = os.path.join(outdir, fname)
            result.save(fpath)
            print(f"Gespeichert: {fpath}")

if __name__ == "__main__":
    main()
