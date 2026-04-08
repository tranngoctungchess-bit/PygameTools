import re
FLOAT_ERROR = 0.0000005
NAMES_TO_HEX = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "grey": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
                }
class ColorTools:
    def name_to_hex(self, name: str) -> str:
        if hex_value := NAMES_TO_HEX.get(name.lower()):
            return hex_value
        raise ValueError(f'"{name}" is not defined as a named color in CSS3')
    def hex_to_rgb(self, hex_value: str):
        int_value = int(self.normalize_hex(hex_value)[1:], 16)
        return int_value >> 16, int_value >> 8 & 0xFF, int_value & 0xFF
    def name_to_rgb(self, name):
        return self.hex_to_rgb(self.name_to_hex(name))
    def normalize_hex(self, hex_value : str):
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
        h, s, l = (float(v) for v in hsl)

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
        r, g, b = (float(v) for v in rgb)

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
aliceblue = "#f0f8ff"
antiquewhite = "#faebd7"
aqua = "#00ffff"
aquamarine = "#7fffd4"
azure = "#f0ffff"
beige = "#f5f5dc"
bisque = "#ffe4c4"
black = "#000000"
blanchedalmond = "#ffebcd"
blue = "#0000ff"
blueviolet = "#8a2be2"
brown = "#a52a2a"
burlywood = "#deb887"
cadetblue = "#5f9ea0"
chartreuse = "#7fff00"
chocolate = "#d2691e"
coral = "#ff7f50"
cornflowerblue = "#6495ed"
cornsilk = "#fff8dc"
crimson = "#dc143c"
cyan = "#00ffff"
darkblue = "#00008b"
darkcyan = "#008b8b"
darkgoldenrod = "#b8860b"
darkgray = "#a9a9a9"
darkgrey = "#a9a9a9"
darkgreen = "#006400"
darkkhaki = "#bdb76b"
darkmagenta = "#8b008b"
darkolivegreen = "#556b2f"
darkorange = "#ff8c00"
darkorchid = "#9932cc"
darkred = "#8b0000"
darksalmon = "#e9967a"
darkseagreen = "#8fbc8f"
darkslateblue = "#483d8b"
darkslategray = "#2f4f4f"
darkslategrey = "#2f4f4f"
darkturquoise = "#00ced1"
darkviolet = "#9400d3"
deeppink = "#ff1493"
deepskyblue = "#00bfff"
dimgray = "#696969"
dimgrey = "#696969"
dodgerblue = "#1e90ff"
firebrick = "#b22222"
floralwhite = "#fffaf0"
forestgreen = "#228b22"
fuchsia = "#ff00ff"
gainsboro = "#dcdcdc"
ghostwhite = "#f8f8ff"
gold = "#ffd700"
goldenrod = "#daa520"
gray = "#808080"
grey = "#808080"
green = "#008000"
greenyellow = "#adff2f"
honeydew = "#f0fff0"
hotpink = "#ff69b4"
indianred = "#cd5c5c"
indigo = "#4b0082"
ivory = "#fffff0"
khaki = "#f0e68c"
lavender = "#e6e6fa"
lavenderblush = "#fff0f5"
lawngreen = "#7cfc00"
lemonchiffon = "#fffacd"
lightblue = "#add8e6"
lightcoral = "#f08080"
lightcyan = "#e0ffff"
lightgoldenrodyellow = "#fafad2"
lightgray = "#d3d3d3"
lightgrey = "#d3d3d3"
lightgreen = "#90ee90"
lightpink = "#ffb6c1"
lightsalmon = "#ffa07a"
lightseagreen = "#20b2aa"
lightskyblue = "#87cefa"
lightslategray = "#778899"
lightslategrey = "#778899"
lightsteelblue = "#b0c4de"
lightyellow = "#ffffe0"
lime = "#00ff00"
limegreen = "#32cd32"
linen = "#faf0e6"
magenta = "#ff00ff"
maroon = "#800000"
mediumaquamarine = "#66cdaa"
mediumblue = "#0000cd"
mediumorchid = "#ba55d3"
mediumpurple = "#9370db"
mediumseagreen = "#3cb371"
mediumslateblue = "#7b68ee"
mediumspringgreen = "#00fa9a"
mediumturquoise = "#48d1cc"
mediumvioletred = "#c71585"
midnightblue = "#191970"
mintcream = "#f5fffa"
mistyrose = "#ffe4e1"
moccasin = "#ffe4b5"
navajowhite = "#ffdead"
navy = "#000080"
oldlace = "#fdf5e6"
olive = "#808000"
olivedrab = "#6b8e23"
orange = "#ffa500"
orangered = "#ff4500"
orchid = "#da70d6"
palegoldenrod = "#eee8aa"
palegreen = "#98fb98"
paleturquoise = "#afeeee"
palevioletred = "#db7093"
papayawhip = "#ffefd5"
peachpuff = "#ffdab9"
peru = "#cd853f"
pink = "#ffc0cb"
plum = "#dda0dd"
powderblue = "#b0e0e6"
purple = "#800080"
red = "#ff0000"
rosybrown = "#bc8f8f"
royalblue = "#4169e1"
saddlebrown = "#8b4513"
salmon = "#fa8072"
sandybrown = "#f4a460"
seagreen = "#2e8b57"
seashell = "#fff5ee"
sienna = "#a0522d"
silver = "#c0c0c0"
skyblue = "#87ceeb"
slateblue = "#6a5acd"
slategray = "#708090"
slategrey = "#708090"
snow = "#fffafa"
springgreen = "#00ff7f"
steelblue = "#4682b4"
tan = "#d2b48c"
teal = "#008080"
thistle = "#d8bfd8"
tomato = "#ff6347"
turquoise = "#40e0d0"
violet = "#ee82ee"
wheat = "#f5deb3"
white = "#ffffff"
whitesmoke = "#f5f5f5"
yellow = "#ffff00"
yellowgreen = "#9acd32"
