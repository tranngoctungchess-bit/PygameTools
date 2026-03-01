from Kernel.PygameRender.RRender import *
from Kernel.Flags.VFlags import *
from Kernel.Flags.UFlags import *
from Kernel.Flags.RFlags import *
def notingfunc(*args, **kwargs):
    pass
renderfunc = {
    ###########
    #UFLAG
    ###########
    text_Is_Bold: set_Bold,
    text_Is_Italic: set_Italic,
    text_Is_Underline: set_Underline,
    text_Is_Antialias: set_Antialias,
    text_Is_Strikethrough: set_Strikethrough,
    text_have_background: set_have_Background,
    ##########
    #VFLAG
    ##########
    bg_widget: fill_bg,
    border: set_border,
    corner_radius: set_border,
    textpack: draw_text,
    ###########
    #RFLAG
    ###########
    Rbg_widget : Remove_bg,
    Rborder : Remove_border,
    Rcorner_radius : corner_radius,
    Rtext_Is_Bold : Remove_textBold,
    Rtext_Is_Italic : Remove_textItalic,
    Rtext_Is_Underline : Remove_textUnderline,
    Rtext_Is_Strikethrough : Remove_textStrikethrough,
    Rtext_Is_Antialias : Remove_textAntialias,
    Rtext_have_background : Remove_textBg,
    RDownrclick: notingfunc,
    RDownlclick: notingfunc,
    RDownscrollmouse: notingfunc,
    RDownscrollup: notingfunc,
    RDownscrolldown: notingfunc,
    RUprclick: notingfunc,
    RUplclick: notingfunc,
    RUpscrollmouse: notingfunc,
    RUpscrollup: notingfunc,
    RUpscrolldown: notingfunc,
    RHover_func : notingfunc,
    Rhover_bg : notingfunc,
    Rpressed_bg: notingfunc,
    RRealeasefunc: notingfunc,
    Rhave_margin: notingfunc,
    #########
    #AFLAG
    #########
    text_auto_resize: text_resize,
    have_margin: notingfunc,
    ########
    #EFLAG
    ########
    Downrclick : notingfunc,
    Downlclick : notingfunc,
    Downscrollmouse : notingfunc,
    Downscrollup : notingfunc,
    Downscrolldown  :notingfunc,
    Uprclick :notingfunc ,
    Uplclick  : notingfunc,
    Upscrollmouse  :notingfunc,
    Upscrollup : notingfunc,
    Upscrolldown: notingfunc,
    hover_bg: notingfunc,
    pressed_bg: notingfunc,
    Hoverfunc: notingfunc,
    Realeasefunc: notingfunc
}