from PIL import Image, ImageDraw
from typing import Optional
from .text_renderer import TextRenderer

def crop_and_resize_image(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """Croppt und skaliert das Bild auf die Zielgröße"""
    img = image.copy()
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    elif img_ratio < target_ratio:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))
    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)

class HorizontalLandscapeLayout:
    def render(self, renderer) -> Image.Image:
        canvas = Image.new('RGB', (renderer.width, renderer.height), 'white')
        draw = ImageDraw.Draw(canvas)
        current_y = renderer.padding
        content_width = renderer.width - 2 * renderer.padding

        # Titel rendern (zentriert, max 2 Zeilen)
        if renderer.title:
            title_renderer = TextRenderer(
                renderer.title, content_width, max_lines=2, font_size=28, align_center=True
            )
            title_renderer.render(draw, renderer.padding, current_y)
            current_y += title_renderer.height + renderer.element_spacing

        # Untertitel rendern (linksbündig, max 3 Zeilen)
        if renderer.subtitle:
            subtitle_renderer = TextRenderer(
                renderer.subtitle, content_width, max_lines=3, font_size=18, align_center=False
            )
            subtitle_renderer.render(draw, renderer.padding, current_y)
            current_y += subtitle_renderer.height + renderer.element_spacing

        # Verfügbare Höhe für Bild berechnen
        available_height = renderer.height - current_y - renderer.padding
        if available_height > 0:
            processed_image = crop_and_resize_image(renderer.image, content_width, available_height)
            canvas.paste(processed_image, (renderer.padding, current_y))
            # QR Code unten rechts auf dem Bild platzieren
            if renderer.qr_image:
                qr_x = renderer.width - renderer.qr_size - renderer.padding
                qr_y = renderer.height - renderer.qr_size - renderer.padding
                canvas.paste(renderer.qr_image, (qr_x, qr_y))
        return canvas

class HorizontalPortraitLayout:
    def __init__(self, ratio: Optional[tuple[float, float]] = None):
        self.ratio = ratio if ratio is not None else (0.5, 0.5)

    def render(self, renderer) -> Image.Image:
        canvas = Image.new('RGB', (renderer.width, renderer.height), 'white')
        draw = ImageDraw.Draw(canvas)
        current_y = renderer.padding
        content_width = renderer.width - 2 * renderer.padding
        # Titel oben mittig rendern (zentriert, max 2 Zeilen)
        if renderer.title:
            title_renderer = TextRenderer(
                renderer.title, content_width, max_lines=2, font_size=28, align_center=True
            )
            title_renderer.render(draw, renderer.padding, current_y)
            current_y += title_renderer.height + renderer.element_spacing
        available_height = renderer.height - current_y - renderer.padding
        if available_height > 0:
            if renderer.subtitle:
                # Konfigurierbares Verhältnis (image:subtitle)
                image_ratio, subtitle_ratio = self.ratio
                total = image_ratio + subtitle_ratio
                image_width = int(content_width * (image_ratio / total)) - renderer.element_spacing // 2
                subtitle_width = content_width - image_width - renderer.element_spacing // 2
                scale_width = image_width / renderer.image.width
                scale_height = available_height / renderer.image.height
                scale = min(scale_width, scale_height)
                new_width = int(renderer.image.width * scale)
                new_height = int(renderer.image.height * scale)
                processed_image = renderer.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                image_x = renderer.padding + (image_width - new_width) // 2
                image_y = current_y + (available_height - new_height) // 2
                canvas.paste(processed_image, (image_x, image_y))
                subtitle_x = renderer.padding + image_width + renderer.element_spacing // 2
                # Subtitle-Top soll exakt auf Bild-Top liegen
                subtitle_y = image_y
                qr_y = image_y + new_height - renderer.qr_size if renderer.qr_image else renderer.height
                max_subtitle_height = qr_y - subtitle_y - renderer.element_spacing if renderer.qr_image else available_height - (subtitle_y - current_y)
                subtitle_renderer = TextRenderer(
                    renderer.subtitle, subtitle_width, max_height=max_subtitle_height, font_size=16, align_center=False
                )
                subtitle_renderer.render(draw, subtitle_x, subtitle_y)
                if renderer.qr_image:
                    right_half_start = subtitle_x
                    right_half_width = subtitle_width
                    qr_x = right_half_start + (right_half_width - renderer.qr_size) // 2
                    canvas.paste(renderer.qr_image, (qr_x, qr_y))
            else:
                scale_width = content_width / renderer.image.width
                scale_height = available_height / renderer.image.height
                scale = min(scale_width, scale_height)
                new_width = int(renderer.image.width * scale)
                new_height = int(renderer.image.height * scale)
                processed_image = renderer.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                image_x = renderer.padding + (content_width - new_width) // 2
                image_y = current_y + (available_height - new_height) // 2
                canvas.paste(processed_image, (image_x, image_y))
                if renderer.qr_image:
                    half_width = content_width // 2
                    right_half_start = renderer.padding + half_width
                    qr_x = right_half_start + (half_width - renderer.qr_size) // 2
                    qr_y = current_y + (available_height - renderer.qr_size) // 2
                    canvas.paste(renderer.qr_image, (qr_x, qr_y))
        return canvas

class VerticalLandscapeLayout:
    def render(self, renderer) -> Image.Image:
        canvas = Image.new('RGB', (renderer.width, renderer.height), 'white')
        draw = ImageDraw.Draw(canvas)
        current_y = renderer.padding
        content_width = renderer.width - 2 * renderer.padding

        # Titel rendern (zentriert, max 2 Zeilen)
        if renderer.title:
            title_renderer = TextRenderer(
                renderer.title, content_width, max_lines=2, font_size=28, align_center=True
            )
            title_renderer.render(draw, renderer.padding, current_y)
            current_y += title_renderer.height + renderer.element_spacing

        # Untertitel rendern (linksbündig, max 3 Zeilen)
        if renderer.subtitle:
            subtitle_renderer = TextRenderer(
                renderer.subtitle, content_width, max_lines=3, font_size=18, align_center=False
            )
            subtitle_renderer.render(draw, renderer.padding, current_y)
            current_y += subtitle_renderer.height + renderer.element_spacing

        # Verfügbare Höhe für Bild/QR-Code bereich berechnen
        available_height = renderer.height - current_y - renderer.padding

        if available_height > 0:
            # Wenn QR-Code vorhanden, Bildhöhe anpassen, damit QR nicht überlappt
            if renderer.qr_image:
                image_height = available_height - renderer.qr_size - renderer.element_spacing
                if image_height < 1:
                    image_height = 1  # Fallback falls zu wenig Platz
            else:
                image_height = available_height

            processed_image = crop_and_resize_image(renderer.image, content_width, image_height)
            image_x = (renderer.width - processed_image.width) // 2
            image_y = current_y
            canvas.paste(processed_image, (image_x, image_y))

            # QR-Code darunter mittig platzieren, falls vorhanden
            if renderer.qr_image:
                qr_y = current_y + image_height + renderer.element_spacing
                qr_x = (renderer.width - renderer.qr_size) // 2
                canvas.paste(renderer.qr_image, (qr_x, qr_y))
        return canvas