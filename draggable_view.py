from Cocoa import NSView

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
