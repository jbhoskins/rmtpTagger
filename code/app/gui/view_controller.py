class Viewer:
    """Abstract class for all viewers in the Observer pattern."""
    def __init__(self):
        pass

    def update(self):
        raise NotImplementedError("All views must implement update()")

class ViewController:
    """Not actually used, but probably should. shows all methods that a
    the subject in the Observer pattern should use implement."""
    def __init__(self):
        self._views = []

    def notifyViewersredraw(self):
        """Redraws all the registered viewers."""
        for view in self._views:
            view.update()

    def registerViewer(self, newView):
        """Add a viewer."""
        self._views.append(newView)

    def deleteViewer(self, viewToDelete):
        """Delete a viewer."""
        self._views.remove(viewToDelete)
