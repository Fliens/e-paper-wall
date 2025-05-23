from PIL import Image, ImageDraw, ImageFont

class TextRenderer:
    def __init__(self, text: str, width: int, max_lines: int = None, max_height: int = None,
                 font_size: int = 24, align_center: bool = False):
        self.text = text
        self.width = width
        self.max_lines = max_lines
        self.max_height = max_height
        self.font_size = font_size
        self.align_center = align_center

        self.font = self._get_font()
        self.line_height = self._measure_line_height()
        self.rendered_text = self._wrap_text()
        self.height = self._calculate_height()

    def _get_font(self):
        try:
            return ImageFont.truetype("arial.ttf", self.font_size)
        except:
            try:
                return ImageFont.truetype("/System/Library/Fonts/Arial.ttf", self.font_size)
            except:
                return ImageFont.load_default()

    def _text_width(self, draw, text):
        return draw.textbbox((0, 0), text, font=self.font)[2]

    def _measure_line_height(self):
        temp_img = Image.new("RGB", (10, 10), "white")
        draw = ImageDraw.Draw(temp_img)
        return draw.textbbox((0, 0), "Ag", font=self.font)[3]

    def _split_long_word(self, word, draw):
        parts, current = [], ''
        for char in word:
            if self._text_width(draw, current + char + "-") > self.width:
                if current:
                    parts.append(current + "-")
                current = char
            else:
                current += char
        if current:
            parts.append(current)
        return parts

    def _wrap_text(self):
        if not self.text:
            return ""

        temp_img = Image.new('RGB', (self.width, 100), 'white')
        draw = ImageDraw.Draw(temp_img)
        lines, current_line = [], ""

        for word in self.text.split():
            parts = self._split_long_word(word, draw) if self._text_width(draw, word) > self.width else [word]
            for part in parts:
                test_line = current_line + (" " if current_line else "") + part
                if self._text_width(draw, test_line) <= self.width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = part
                    if self._limit_reached(len(lines) + 1):
                        return self._truncate(lines, draw)

        if current_line:
            lines.append(current_line)

        while self._limit_reached(len(lines)):
            lines.pop()
            return self._truncate(lines, draw)

        return '\n'.join(lines)

    def _limit_reached(self, line_count):
        if self.max_lines and line_count > self.max_lines:
            return True
        if self.max_height and (line_count * self.line_height) > self.max_height:
            return True
        return False

    def _truncate(self, lines, draw):
        if not lines:
            return ""
        last = lines[-1].rstrip('-').rstrip()
        while last:
            test_line = last + "..."
            if self._text_width(draw, test_line) <= self.width:
                lines[-1] = test_line
                break
            last = last[:-1]
        return '\n'.join(lines)

    def _calculate_height(self):
        return self.rendered_text.count('\n') * self.line_height + self.line_height if self.rendered_text else 0

    def render(self, draw, x, y, color='black'):
        if not self.rendered_text:
            return
        lines = self.rendered_text.split('\n')
        for i, line in enumerate(lines):
            line_y = y + i * self.line_height
            if self.align_center:
                line_width = self._text_width(draw, line)
                line_x = x + (self.width - line_width) // 2
            else:
                line_x = x
            draw.text((line_x, line_y), line, fill=color, font=self.font)