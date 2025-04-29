import sys
from Quartz.CoreGraphics import CGColorCreateGenericRGB
from AppKit import NSButton, NSStackView, NSUserInterfaceLayoutOrientationVertical
from Cocoa import (
    NSApplication,
    NSStatusBar,
    NSVariableStatusItemLength,
    NSImage,
    NSMenu,
    NSMenuItem,
    NSWindow,
    NSView,
    NSMakeRect,
    NSTextField,
    NSObject,
    NSEvent,
    NSScreen,
    NSApplicationActivationPolicyProhibited,
    NSWindowStyleMaskTitled,
    NSWindowStyleMaskClosable,
    NSWindowStyleMaskResizable,
    NSWindowStyleMaskBorderless,
    NSColor,
    NSVisualEffectView,
    NSVisualEffectMaterialPopover,
    NSVisualEffectBlendingModeBehindWindow
)

# DraggableView enables dragging a borderless window
class DraggableView(NSView):
    def mouseDown_(self, event):
        self._initialClickLocation = self.convertPoint_fromView_(event.locationInWindow(), None)
        self._initialWindowOrigin = self.window().frame().origin

    def mouseDragged_(self, event):
        currentLocation = self.convertPoint_fromView_(event.locationInWindow(), None)
        dx = currentLocation.x - self._initialClickLocation.x
        dy = currentLocation.y - self._initialClickLocation.y
        window = self.window()
        frame = window.frame()
        newOrigin = (frame.origin.x + dx, frame.origin.y + dy)
        window.setFrameOrigin_(newOrigin)

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        self.window_visible = False

        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.setTitle_("📋")
        self.status_item.button().setAction_("toggleWindow:")
        self.status_item.button().setTarget_(self)

        self.createMenu()

        popup_width, popup_height = 360, 450  # macOS lookup-style size
        self.popup_width = popup_width
        self.popup_height = popup_height

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(0, 0, popup_width, popup_height),
            NSWindowStyleMaskBorderless,
            2,
            False
        )
        self.window.setLevel_(3)
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.setHasShadow_(False)
        self.window.setMovableByWindowBackground_(False)

        # Visual effect view for blur background and rounded corners
        effect_view = NSVisualEffectView.alloc().initWithFrame_(NSMakeRect(0, 0, popup_width, popup_height))
        effect_view.setMaterial_(NSVisualEffectMaterialPopover)
        effect_view.setBlendingMode_(NSVisualEffectBlendingModeBehindWindow)
        effect_view.setState_(1)
        effect_view.setWantsLayer_(True)
        effect_view.layer().setCornerRadius_(10.0)
        effect_view.layer().setMasksToBounds_(True)
        effect_view.layer().setBorderWidth_(0.5)
        gray_color = CGColorCreateGenericRGB(1, 1, 1, 0.2)  # RGB + Alpha
        effect_view.layer().setBorderColor_(gray_color)

        # Add drag support via DraggableView as subview
        drag_view = DraggableView.alloc().initWithFrame_(NSMakeRect(0, 0, popup_width, popup_height))
        effect_view.addSubview_(drag_view)

        # Add top-left label "dupe" with custom color and italic font
        label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, popup_height - 32, 100, 24))
        label.setStringValue_("dupe")
        label.setBordered_(False)
        label.setEditable_(False)
        label.setDrawsBackground_(False)
        label.setFont_(label.font().fontWithSize_(16))
        label.setTextColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 1, 0.5))  # Custom RGB color
        effect_view.addSubview_(label)

        # Add a divider line
        divider = NSView.alloc().initWithFrame_(NSMakeRect(0, popup_height - 35, popup_width, 1))
        divider.setWantsLayer_(True)
        divider.layer().setBackgroundColor_(CGColorCreateGenericRGB(1, 1, 1, 0.2))  # Light gray color
        effect_view.addSubview_(divider)

        # Add close button to top-right corner
        close_button = NSButton.alloc().initWithFrame_(NSMakeRect(popup_width - 55, popup_height - 32, 50, 25))
        close_button.setTitle_("close")
        close_button.setBezelStyle_(4)  # Rounded button style
        close_button.setTarget_(self)
        close_button.setAction_("closeWindow:")
        effect_view.addSubview_(close_button)

        self.window.setContentView_(effect_view)
        self.window.setDelegate_(self)

    def createMenu(self):
        self.menu = NSMenu.alloc().init()

        toggle_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Toggle Window", "toggleWindow:", ""
        )
        self.menu.addItem_(toggle_item)

        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit", "quitApp:", ""
        )
        self.menu.addItem_(quit_item)

        self.status_item.setMenu_(self.menu)

    def toggleWindow_(self, sender):
        if self.window_visible:
            self.window.orderOut_(None)
        else:
            self.showWindowCentered()
        self.window_visible = not self.window_visible

    def showWindowCentered(self):
        screen_frame = NSScreen.mainScreen().frame()
        screen_width = screen_frame.size.width
        screen_height = screen_frame.size.height

        window_x = (screen_width - self.popup_width) / 2
        window_y = (screen_height - self.popup_height) / 2
        self.window.setFrameTopLeftPoint_((window_x, window_y + self.popup_height))
        self.window.makeKeyAndOrderFront_(None)

    def windowShouldClose_(self, sender):
        self.window.orderOut_(None)
        self.window_visible = False

    def quitApp_(self, sender):
        NSApplication.sharedApplication().terminate_(None)

    # Close the window (popup) when the close button is clicked
    def closeWindow_(self, sender):
        self.window.orderOut_(None)
        self.window_visible = False

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyProhibited)
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()