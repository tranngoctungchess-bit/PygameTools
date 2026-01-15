from Kernel import color
FLOAT_ERROR = 0.0000005
class ColorTools:
    def name_to_hex(self, name: str) -> str:
        if hex_value := NAMES_TO_HEX.get(name.lower()):
            return hex_value
        raise ValueError(f'"{name}" is not defined as a named color in CSS3')
    def hex_to_rgb(self, hex_value: str):
        int_value = int(normalize_hex(hex_value)[1:], 16)
        return int_value >> 16, int_value >> 8 & 0xFF, int_value & 0xFF
    def name_to_rgb(self, name, spec='CSS3'):
        return hex_to_rgb(name_to_hex(name, spec=spec))
    def normolize_hex(self, hex_value : str):
        if (match := re.compile(r"^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$").match(hex_value)) is None:
            raise ValueError(f'"{hex_value}" is not a valid hexadecimal color value.')
        hex_digits = match.group(1)
        if len(hex_digits) == 3:
            hex_digits = "".join(2 * s for s in hex_digits)
        return f"#{hex_digits.lower()}"

    def hue_to_rgb(self, v1, v2, vH):

        while vH < 0: vH += 1
        while vH > 1: vH -= 1

        if 6 * vH < 1: return v1 + (v2 - v1) * 6 * vH
        if 2 * vH < 1: return v2
        if 3 * vH < 2: return v1 + (v2 - v1) * ((2.0 / 3) - vH) * 6

        return v1
    def hsl_to_rgb(self, hsl):
        h, s, l = [float(v) for v in hsl]

        if not (0.0 - FLOAT_ERROR <= s <= 1.0 + FLOAT_ERROR):
            raise ValueError("Saturation must be between 0 and 1.")
        if not (0.0 - FLOAT_ERROR <= l <= 1.0 + FLOAT_ERROR):
            raise ValueError("Lightness must be between 0 and 1.")

        if s == 0:
            return l, l, l

        if l < 0.5:
            v2 = l * (1.0 + s)
        else:
            v2 = (l + s) - (s * l)

        v1 = 2.0 * l - v2

        r = self.hue_to_rgb(v1, v2, h + (1.0 / 3))
        g = self.hue_to_rgb(v1, v2, h)
        b = self.hue_to_rgb(v1, v2, h - (1.0 / 3))

        return r, g, b

    def rgb_to_hsl(self, rgb):
        r, g, b = [float(v) for v in rgb]

        for name, v in {'Red': r, 'Green': g, 'Blue': b}.items():
            if not (0 - FLOAT_ERROR <= v <= 1 + FLOAT_ERROR):
                raise ValueError("%s must be between 0 and 1. You provided %r."
                                 % (name, v))

        vmin = min(r, g, b)  ## Min. value of RGB
        vmax = max(r, g, b)  ## Max. value of RGB
        diff = vmax - vmin  ## Delta RGB value

        vsum = vmin + vmax

        l = vsum / 2

        if diff < FLOAT_ERROR:
            return 0.0, 0.0, l

        ##
        ## Chromatic data...
        ##

        ## Saturation
        if l < 0.5:
            s = diff / vsum
        else:
            s = diff / (2.0 - vsum)

        dr = (((vmax - r) / 6) + (diff / 2)) / diff
        dg = (((vmax - g) / 6) + (diff / 2)) / diff
        db = (((vmax - b) / 6) + (diff / 2)) / diff

        if r == vmax:
            h = db - dg
        elif g == vmax:
            h = (1.0 / 3) + dr - db
        elif b == vmax:
            h = (2.0 / 3) + dg - dr

        if h < 0: h += 1
        if h > 1: h -= 1

        return h, s, l


class GradientGenerator:
    def linear_gradient(self, color_start, color_end, steps):
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1)
            # Trộn màu
            r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
            gradient.append((r, g, b))
        return gradient

    def multi_gradient(self, colors, steps):
        gradient = []
        segments = len(colors) - 1
        steps_per_segment = steps // segments

        for i in range(segments):
            segment_grad = self.linear_gradient(
                colors[i], colors[i + 1], steps_per_segment
            )
            gradient.extend(segment_grad)

        return gradient