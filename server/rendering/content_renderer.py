from PIL import Image
from typing import Optional, Tuple
import qrcode
from .layouts import HorizontalLandscapeLayout, HorizontalPortraitLayout, VerticalLandscapeLayout

class ContentRenderer:
    def __init__(self, resolution: Tuple[int, int], image: Image.Image, title: Optional[str] = None, subtitle: Optional[str] = None, url: Optional[str] = None, 
                 padding: int = 20, element_spacing: int = 15, qr_size: int = 100):
        """
        E-Paper Layout Renderer
        
        Args:
            resolution: Tuple (width, height) der E-Paper Auflösung
            image: PIL Image Objekt
            title: Titel Text (optional)
            subtitle: Untertitel Text (optional)
            url: URL für QR Code (optional)
            padding: Abstand zum Rand
            element_spacing: Abstand zwischen Elementen
            qr_size: Größe des QR Codes
        """
        self.width, self.height = resolution
        self.image = image
        self.title = title
        self.subtitle = subtitle
        self.url = url
        self.padding = padding
        self.element_spacing = element_spacing
        self.qr_size = qr_size
        
        # Display-Orientierung bestimmen
        self.display_horizontal = self.width > self.height
        
        # Bild-Orientierung bestimmen
        img_width, img_height = self.image.size
        self.image_landscape = img_width > img_height
        
        # QR Code generieren falls URL vorhanden
        self.qr_image = self._generate_qr_code() if self.url else None
        
    def _generate_qr_code(self) -> Image.Image:
        """Generiert QR Code aus URL"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=1,
        )
        qr.add_data(self.url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        return qr_img.resize((self.qr_size, self.qr_size))
    
    def _layout_horizontal_landscape(self) -> Image.Image:
        print("Horizontal Landscape Layout")
        return HorizontalLandscapeLayout().render(self)
    
    def _layout_horizontal_portrait(self) -> Image.Image:
        print("Horizontal Portrait Layout")
        return HorizontalPortraitLayout().render(self)
    
    def _layout_vertical_landscape(self) -> Image.Image:
        print("Vertical Landscape Layout")
        return VerticalLandscapeLayout().render(self)
    
    def _layout_vertical_portrait(self) -> Image.Image:
        print("Vertical Portrait Layout")
        # Nutze das horizontale Portrait-Layout auch für vertikal/portrait
        return VerticalLandscapeLayout().render(self)
    
    def render(self):
        """Rendert das Layout basierend auf Display- und Bild-Orientierung"""
        if self.display_horizontal and self.image_landscape:
            return self._layout_horizontal_landscape()
        elif self.display_horizontal and not self.image_landscape:
            return self._layout_horizontal_portrait()
        elif not self.display_horizontal and self.image_landscape:
            return self._layout_vertical_landscape()
        else:  # vertical display, portrait image
            return self._layout_vertical_portrait()


# Beispiel für die Verwendung:
if __name__ == "__main__":
    # Beispiel-Setup
    #resolution = (800, 480)  # Horizontales E-Paper Display
    resolution = (480, 800)  # Horizontales E-Paper Display
    from PIL import Image
    example_image = Image.open("landscape.jpg")  # Beispielbild
    renderer = ContentRenderer(
        resolution=resolution,
        image=example_image,
        title="Das ist ein sehr langer Titel der über mehrere Zeilen gehen könnte",
        subtitle="Dies ist ein Untertitel mit zusätzlichen Informationen die auch länger sein können.",
        url="https://example.com"
    )
    result = renderer.render()
    result.show()