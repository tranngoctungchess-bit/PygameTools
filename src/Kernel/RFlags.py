from Kernel.UFlags import *
from Kernel.VFlags import *
"""
RUFLAGS
"""
Rtext_Is_Bold = text_Is_Bold + 2000
Rtext_Is_Italic = text_Is_Italic + 2000
Rtext_Is_Underline = text_Is_Underline + 2000
Rtext_Is_Strikethrough = text_Is_Strikethrough + 2000
Rtext_Is_Antialias = text_Is_Antialias + 2000
Rtext_have_background = text_have_background + 2000
Rhave_margin = have_margin + 2000
"""
RVflags
"""
Rbg_widget = bg_widget + 2000
Rborder = border + 2000
Rcorner_radius = corner_radius + 2000
Rtextpack = textpack + 2000
RDownrclick = Downrclick + 2000
RDownlclick = Downlclick + 2000
RDownscrollmouse = Downscrollmouse + 2000
RDownscrollup = Downscrollup + 2000
RDownscrolldown = Downscrolldown + 2000
RUprclick = Uprclick + 2000
RUplclick =  Uplclick + 2000
RUpscrollmouse = Upscrollmouse + 2000
RUpscrollup = Upscrollup + 2000
RUpscrolldown = Upscrolldown + 2000
Rhover_bg = hover_bg + 2000
Rpressed_bg = pressed_bg + 2000
RHover_func = Hoverfunc + 2000
RRealeasefunc = Realeasefunc + 2000
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
    have_margin: Rhave_margin
}
rflags_to_vflags = {
    bg_widget: Rbg_widget,
    border: Rborder,
    corner_radius: Rcorner_radius,
    textpack: Rtextpack,
    Downrclick: RDownrclick,
    Downlclick: RDownlclick,
    Downscrollmouse: RDownscrollmouse,
    Downscrolldown: RDownscrolldown,
    Downscrollup: RDownscrollup,
    Uprclick: RUprclick,
    Uplclick: RUplclick,
    Upscrollmouse: RUpscrollmouse,
    Upscrollup: RUpscrollup,
    Upscrolldown: RUpscrolldown,
    Hoverfunc: RHover_func,
    Realeasefunc: RRealeasefunc
}
