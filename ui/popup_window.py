from Cocoa import NSWindow, NSMakeRect, NSWindowStyleMaskBorderless, NSColor
from draggable_view import DraggableView
from ui.components import create_effect_view

def create_popup_window(delegate):
    popup_width, popup_height = 360, 450
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(0, 0, popup_width, popup_height),
        NSWindowStyleMaskBorderless,
        2,
        False
    )
    window.setLevel_(3)
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.setHasShadow_(False)
    window.setMovableByWindowBackground_(False)

    effect_view = create_effect_view(popup_width, popup_height, delegate)
    window.setContentView_(effect_view)
    window.setDelegate_(delegate)

    return window
