from Cocoa import NSButton, NSMakeRect, NSTextField, NSView, NSVisualEffectView, NSVisualEffectMaterialPopover, NSVisualEffectBlendingModeBehindWindow, NSColor
from Quartz.CoreGraphics import CGColorCreateGenericRGB
from draggable_view import DraggableView

def create_effect_view(width, height, delegate):
    effect_view = NSVisualEffectView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    effect_view.setMaterial_(NSVisualEffectMaterialPopover)
    effect_view.setBlendingMode_(NSVisualEffectBlendingModeBehindWindow)
    effect_view.setState_(1)
    effect_view.setWantsLayer_(True)
    effect_view.layer().setCornerRadius_(10.0)
    effect_view.layer().setMasksToBounds_(True)
    effect_view.layer().setBorderWidth_(0.5)
    effect_view.layer().setBorderColor_(CGColorCreateGenericRGB(1, 1, 1, 0.2))

    drag_view = DraggableView.alloc().initWithFrame_(NSMakeRect(0, 0, width, height))
    effect_view.addSubview_(drag_view)

    label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, height - 32, 100, 24))
    label.setStringValue_("dupe")
    label.setBordered_(False)
    label.setEditable_(False)
    label.setDrawsBackground_(False)
    label.setFont_(label.font().fontWithSize_(16))
    label.setTextColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 1, 0.5))
    effect_view.addSubview_(label)

    divider = NSView.alloc().initWithFrame_(NSMakeRect(0, height - 35, width, 1))
    divider.setWantsLayer_(True)
    divider.layer().setBackgroundColor_(CGColorCreateGenericRGB(1, 1, 1, 0.2))
    effect_view.addSubview_(divider)

    close_button = NSButton.alloc().initWithFrame_(NSMakeRect(width - 55, height - 32, 50, 25))
    close_button.setTitle_("close")
    close_button.setBezelStyle_(4)
    close_button.setTarget_(delegate)
    close_button.setAction_("closeWindow:")
    effect_view.addSubview_(close_button)

    for idx, item in enumerate(delegate.clipboard_manager.history):
        button = NSButton.alloc().initWithFrame_(NSMakeRect(10, height - 70 - idx * 40, width - 20, 30))
        button.setTitle_(item[:50])
        button.setBezelStyle_(4)
        button.setTarget_(delegate.clipboard_manager)
        button.setAction_("recopy:")
        button.setTag_(idx)
        effect_view.addSubview_(button)

    return effect_view