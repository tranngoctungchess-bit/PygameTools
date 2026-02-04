from Kernel.PygameRender.Render import *
from Kernel.UFlags import *
from Kernel.VFlags import *
from Kernel.RFlags import *
from Kernel.PygameRender.RRender import *
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
    bg_color: fill_bg,
    border: set_border,
    corner_radius: set_border,
    textpack: draw_text,
    ###########
    #RFLAG
    ###########
    Rbg_color : Remove_bg,
    Rborder : Remove_border,
    Rcorner_radius : corner_radius,
    Rtext_Is_Bold : Remove_textBold,
    Rtext_Is_Italic : Remove_textItalic,
    Rtext_Is_Underline : Remove_textUnderline,
    Rtext_Is_Strikethrough : Remove_textStrikethrough,
    Rtext_Is_Antialias : Remove_textAntialias,
    Rtext_have_background : Remove_textBg,
    #########
    #AFLAG
    #########
    text_auto_resize: text_resize
}