import threading

"""
This module helps you use PyQt in Houdini's GUI.

Rules when using multiple threads:
- Don't directly run code that accesses PyQt.  Instead, call queueCommand
  to queue a command to run on the thread dedicated to PyQt apps.
- Don't import PyQt4 from any code that isn't running on the PyQt thread.
- Don't create QtGui.QApplication's.  Instead, call getApplication.
- Don't write/print anything to stdout/stderr (at least not when there's a
  Python shell open in Houdini), or Houdini will hang.
"""

# Set this variable to False to run PyQt in the main thread.  If it runs in
# the main thread, the rest of Houdini will be blocked until the application
# ends.
use_separate_thread = True

__command_queue = []
__command_queue_lock = threading.Lock()
__command_queue_event = threading.Event()

__pyqt_thread = None
def queueCommand(callable, arguments=()):
    """Queue up a command to run on the PyQt thread."""
    if use_separate_thread == False:
        callable(*arguments)
        return

    # Start up the PyQt thread if it's not already running.
    global __pyqt_thread
    if __pyqt_thread is None:
        __pyqt_thread = threading.Thread(target=__pyQtThreadMain)
        __pyqt_thread.start()

    __command_queue_lock.acquire()
    __command_queue.append((callable, arguments))
    __command_queue_lock.release()

    # Signal the PyQt thread to run the task.
    __command_queue_event.set()

def __pyQtThreadMain():
    """This function is the starting point for the PyQt thread."""

    # It's important that we import PyQt4 only from the PyQt thread, and not
    # from another thread.
    from PyQt4 import QtCore
    from PyQt4 import QtGui

    while True:
        # Wait for the main thread to signal us.
        __command_queue_event.wait()

        # Remove the command from the stack and reset the event.
        __command_queue_lock.acquire()
        command = __command_queue.pop()
        __command_queue_event.clear()
        __command_queue_lock.release()

        # Run the command.
        command[0].__call__(*command[1])

__pyqt_app = None
def getApplication():
    """Return the QtGui.QApplication.  Use this function instead of creating
       PyQt threads manually.  Do not call this function from anything other
       than the PyQt thread."""
    # This function may only be called from the PyQt thread.
    from PyQt4 import QtCore
    from PyQt4 import QtGui

    # We're careful not to create more than one QApplication.
    global __pyqt_app
    if __pyqt_app is None:
        __pyqt_app = QtGui.QApplication(['houdini'])
    return __pyqt_app

