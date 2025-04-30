from Cocoa import NSObject, NSStatusBar, NSVariableStatusItemLength, NSMenu, NSMenuItem, NSApplication, NSEventTypeRightMouseDown, NSEventMaskLeftMouseDown, NSEventMaskRightMouseDown
from ui.popup_window import create_popup_window

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        from Cocoa import NSScreen

        self.window_visible = False
        self.menu = NSMenu.alloc().init()
        self.popup_window = create_popup_window(self)

        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.setTitle_("📋")
        self.status_item.button().setAction_("toggleWindow:")
        self.status_item.button().setTarget_(self)
        self.status_item.button().sendActionOn_(NSEventMaskLeftMouseDown | NSEventMaskRightMouseDown)

        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "quitApp:", "")
        quit_item.setTarget_(self)
        self.menu.addItem_(quit_item)

    def toggleWindow_(self, sender):
        current_event = NSApplication.sharedApplication().currentEvent()
        if current_event and current_event.type() == NSEventTypeRightMouseDown:
            self.status_item.popUpStatusItemMenu_(self.menu)
            return

        if self.window_visible:
            self.popup_window.orderOut_(None)
        else:
            self.showWindowCentered()
        self.window_visible = not self.window_visible

    def showWindowCentered(self):
        from Cocoa import NSScreen

        screen_frame = NSScreen.mainScreen().frame()
        screen_width = screen_frame.size.width
        screen_height = screen_frame.size.height
        popup_width, popup_height = self.popup_window.frame().size.width, self.popup_window.frame().size.height

        window_x = (screen_width - popup_width) / 2
        window_y = (screen_height - popup_height) / 2
        self.popup_window.setFrameTopLeftPoint_((window_x, window_y + popup_height))
        self.popup_window.makeKeyAndOrderFront_(None)

    def quitApp_(self, sender):
        NSApplication.sharedApplication().terminate_(None)

    def closeWindow_(self, sender):
        self.popup_window.orderOut_(None)
        self.window_visible = False
