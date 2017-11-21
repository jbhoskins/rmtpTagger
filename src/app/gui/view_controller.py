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

    def notify_viewers_redraw(self):
        """Redraws all the registered viewers."""
        for view in self._views:
            view.update()

    def register_viewer(self, newView):
        """Add a viewer."""
        self._views.append(newView)

    def delete_viewer(self, viewToDelete):
        """Delete a viewer."""
        self._views.remove(viewToDelete)


class Stylable:
    """Abstract class that is identical to a viewer, the difference being its
    wording for easier readibility."""
    def __init__(self):
        pass

    def style(self):
        raise NotImplementedError("All Stylables must implement style()")


class Styler(ViewController):
    def __init__(self):
        ViewController.__init__(self)

    def notify_viewers_redraw(self):
        for stylable in self._views:
            stylable.style(self)
            print("success")

