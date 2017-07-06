""" class that controls all of the updating done on the screen."""


class Viewer:
    def __init__(self):
        pass

    def update(self):
        raise NotImplementedError("All views must implement update()")

class ViewController:
    def __init__(self):
        self._views = []

    def notifyViewersredraw(self):
        for view in self._views:
            view.update()

    def registerViewer(self, newView):
        self._views.append(newView)

    def deleteViewer(self, viewToDelete):
        self._views.remove(viewToDelete)
