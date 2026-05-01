##########
#COMMON
##########

bg_widget = 1001 # Not for Label
border = bg_widget + 1 # Not for Label
corner_radius = border + 1 # Not for Label
#########
#LABEL
########
textpack = corner_radius + 1
##########
#BUTTON
##########
Downrclick = textpack + 1
Downlclick = Downrclick + 1
Downscrollmouse = Downlclick + 1
Downscrollup = Downscrollmouse + 1
Downscrolldown = Downscrollup + 1
Uprclick = Downscrolldown + 1
Uplclick =  Uprclick + 1
Upscrollmouse = Uplclick + 1
Upscrollup = Upscrollmouse + 1
Upscrolldown = Upscrollup + 1
hover_bg = Upscrolldown + 1
pressed_bg = hover_bg + 1
Hoverfunc = pressed_bg + 1
Realeasefunc = Hoverfunc + 1
Enterfunc = Realeasefunc + 1