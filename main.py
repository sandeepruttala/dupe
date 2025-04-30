from Cocoa import NSApplication, NSApplicationActivationPolicyProhibited
from app_delegate import AppDelegate

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyProhibited)
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()
