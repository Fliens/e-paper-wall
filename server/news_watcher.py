import requests
from PIL import Image
from io import BytesIO
from rendering.content_renderer import ContentRenderer
from rendering.image_converter import ImageConverter, Palette

NEWS_URL = "https://www.tagesschau.de/api2u/news/?regions=3"
RESOLUTION = (800, 480)  # Passe ggf. an dein Display an
#RESOLUTION = (480, 800)  # Passe ggf. an dein Display an


def get_latest_news():
    resp = requests.get(NEWS_URL)
    resp.raise_for_status()
    data = resp.json()
    if not data["news"]:
        return None
    return data["news"][0]

def download_image(news):
    variants = news["teaserImage"]["imageVariants"]
    url = variants.get("original") or variants.get("16x9-960")
    if not url:
        url = next(iter(variants.values()))
    resp = requests.get(url)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))


def show_last_three_news():
    try:
        resp = requests.get(NEWS_URL)
        resp.raise_for_status()
        data = resp.json()

        news_list = data.get("news", [])[:3]
        if not news_list:
            print("No news found.")
            return
        
        for news in news_list:
            print(f"News: {news['title']}")
            image = download_image(news)
            title = news["title"]
            subtitle = news.get("firstSentence") or news.get("topline")
            url = news.get("detailsweb") or news.get("shareURL")
            renderer = ContentRenderer(
                resolution=RESOLUTION,
                image=image,
                title=title,
                subtitle=subtitle,
                url=url
            )
            result = renderer.render()

            # Convert the rendered result image using all palettes
            converter = ImageConverter()
            palettes = list(Palette)
            converted_images = []
            for palette in palettes:
                converted = converter.convert(result, palette)
                # Add a label to the image for the palette name
                labeled = converted.convert("RGB")
                converted_images.append(labeled)

            # Stack all converted images vertically
            total_height = sum(img.height for img in converted_images)
            max_width = max(img.width for img in converted_images)
            big_image = Image.new("RGB", (max_width, total_height), (255,255,255))
            y = 0
            for img in converted_images:
                big_image.paste(img, (0, y))
                y += img.height

            big_image.show()  # Or big_image.save("output_palettes.png")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    show_last_three_news()
