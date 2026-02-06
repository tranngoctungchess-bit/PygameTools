from Kernel.Flags.UFlags import *
from Kernel.Flags.VFlags import *
"""
RUFLAGS
"""
Rtext_Is_Bold = text_Is_Bold + 2000
Rtext_Is_Italic = text_Is_Italic + 2000
Rtext_Is_Underline = text_Is_Underline + 2000
Rtext_Is_Strikethrough = text_Is_Strikethrough + 2000
Rtext_Is_Antialias = text_Is_Antialias + 2000
Rtext_have_background = text_have_background + 2000
"""
RVflags
"""
Rbg_color = bg_color + 2000
Rborder = border + 2000
Rcorner_radius = corner_radius + 2000
Rtextpack = textpack + 2000
"""
Link Rflag to Uflag, Vflag
"""
rflags_to_uflags = {
    text_Is_Bold: Rtext_Is_Bold,
    text_Is_Italic: Rtext_Is_Italic,
    text_Is_Underline: Rtext_Is_Underline,
    text_Is_Strikethrough: Rtext_Is_Strikethrough,
    text_Is_Antialias: Rtext_Is_Antialias,
    text_have_background: Rtext_have_background,
}
rflags_to_vflags = {
    bg_color: Rbg_color,
    border: Rborder,
    corner_radius: Rcorner_radius,
    textpack: Rtextpack,
}
