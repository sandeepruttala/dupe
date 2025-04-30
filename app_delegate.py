from Cocoa import NSObject, NSStatusBar, NSVariableStatusItemLength, NSMenu, NSMenuItem, NSApplication, NSTimer, NSEventTypeRightMouseDown, NSEventMaskLeftMouseDown, NSEventMaskRightMouseDown
from ui.popup_window import create_popup_window
from clipboard_manager import ClipboardManager

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        self.window_visible = False
        self.clipboard_manager = ClipboardManager()
        # Set the update callback to refresh the UI when clipboard changes
        self.clipboard_manager.setUpdateCallback(self.refreshWindow)
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.5, self.clipboard_manager, "pollClipboard:", None, True
        )

        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.setTitle_("📋")
        self.status_item.button().setAction_("toggleWindow:")
        self.status_item.button().setTarget_(self)
        self.status_item.button().sendActionOn_(NSEventMaskLeftMouseDown | NSEventMaskRightMouseDown)

        self.menu = NSMenu.alloc().init()
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "quitApp:", "")
        quit_item.setTarget_(self)
        self.menu.addItem_(quit_item)

        self.popup_window = create_popup_window(self)

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
        window_width, window_height = self.popup_window.frame().size.width, self.popup_window.frame().size.height
        x = (screen_frame.size.width - window_width) / 2
        y = (screen_frame.size.height - window_height) / 2
        self.popup_window.setFrameTopLeftPoint_((x, y + window_height))
        self.popup_window.makeKeyAndOrderFront_(None)

    def quitApp_(self, sender):
        NSApplication.sharedApplication().terminate_(None)

    def closeWindow_(self, sender):
        self.popup_window.orderOut_(None)
        self.window_visible = False
    
    def refreshWindow(self):
        # Create a new window with updated clipboard items
        old_window = self.popup_window
        self.popup_window = create_popup_window(self)
        
        # If the window is visible, update its position and show the new one
        if self.window_visible:
            frame = old_window.frame()
            self.popup_window.setFrame_display_(frame, True)
            self.popup_window.makeKeyAndOrderFront_(None)
            old_window.orderOut_(None)
    