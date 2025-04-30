from AppKit import NSPasteboard

class ClipboardManager:
    def __init__(self):
        self.pasteboard = NSPasteboard.generalPasteboard()
        self.change_count = self.pasteboard.changeCount()
        self.history = []
        self.update_callback = None  # 🔁 Add callback reference

    def setUpdateCallback(self, callback):
        self.update_callback = callback

    def pollClipboard_(self, timer):
        new_count = self.pasteboard.changeCount()
        if new_count != self.change_count:
            self.change_count = new_count
            content = self.pasteboard.stringForType_("public.utf8-plain-text")
            if content and (len(self.history) == 0 or content != self.history[0]):
                self.history.insert(0, content)
                self.history = self.history[:5]
                if self.update_callback:
                    self.update_callback()  # 🔁 Notify UI
    
    def recopy_(self, sender):
        # Get the index from the button's tag
        index = sender.tag()
        if index < len(self.history):
            # Copy the selected item back to the clipboard
            self.pasteboard.clearContents()
            self.pasteboard.setString_forType_(self.history[index], "public.utf8-plain-text")
