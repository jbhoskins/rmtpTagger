"""Experimental Template editor interface, to allow the defining, removal, and editing of tag templates
without manually editing the text file. Incomplete."""
from app.gui.popup_window import PopupWindow
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

import app.backend.tag_templates as templates


class TemplateEditor(PopupWindow):
    """A popup window that gives access to the template configuration file. """
    def __init__(self, root):
        # This widget might benefit from the observer pattern as well.
        self.__template_index = templates.TemplateIndex()
        PopupWindow.__init__(self, root)
    
        self.bind("<Double-Button-1>", self.edit_tag)

    def _add_widgets(self):
        """ Called in superclass, adds all widgets to itself."""

        headings = ("name", "front tag", "back tag", "arguments")
        self.tree = ttk.Treeview(self, columns=headings, show="headings")

        for col in headings:
            self.tree.heading(col, text=col.title())
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Need this frame to pack the buttons neatly centered below the table.
        button_frame = tk.Frame(self)

        tk.Button(button_frame, text="add",
                  command=self.add_tag).pack(side=tk.LEFT)
        tk.Button(button_frame, text="edit", command=self.edit_tag).pack(side=tk.LEFT)
        tk.Button(button_frame, text="delete",
                  command=self.delete_tag).pack(side=tk.LEFT)
        tk.Button(button_frame, text="ok", command=self.close_and_commit).pack(side=tk.LEFT)
        tk.Button(button_frame, text="cancel", command=self.close).pack(side=tk.LEFT)

        button_frame.pack(expand=True)
        self.update_tags()

    def edit_tag(self, event=None):
        """Opens another popup window that allows the user to edit the selected
        template."""
        # Note: event passed as it is needed for the binding to mouseclick. 
        selection = self.tree.focus()
        index = self.tree.index(selection)
        
        tmp = AddTemplateEditor(self, self.__template_index, index)
        
        # get the values of the selected template to fill the defaults of the
        # new popup window
        name = self.__template_index.get_names()[index]
        front_tag = self.__template_index.get_values()[index].get_front()
        end_tag = self.__template_index.get_values()[index].get_back()
        arguments = self.__template_index.get_values()[index].get_arguments()

        tmp.set_defaults(name, front_tag, end_tag, arguments)

    def update_tags(self):
        """Populate the listbox with the names of the templates in the
        template index."""

        # Delete all the templates in the view.
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Populate the tree view with templates.
        for template in self.__template_index.get_templates():
            self.tree.insert("", tk.END, text=template[0],
                             values=(template[0],) + template[1].get_tuple())

    def close_and_commit(self):
        """Write the current index to file, and close the popup window."""
        
        f = open("../META/tagTemplatesBackup.txt", "w")
        f.write(self.__template_index.get_file_string())
        f.close()
        print("Successfully updated tags")

        # grab_release allows the user to iteract with other windows again.
        self.grab_release()
        self.destroy()

    def close(self):
        """Closes the window."""
        # grab_release allows the user to interact with other windows again.
        self.grab_release()
        self.destroy()

    def delete_tag(self):
        """Delete the currently selected template."""
        
        # This actually can be undone if we add a cancel button - this is
        # probably a better solution.
        if tk.messagebox.askquestion("Delete Warning", "Are you sure you"+\
            "want to delete this template? This cannot be undone.") == "no":
            return
        
        selection = self.tree.focus()
        index = self.tree.index(selection)
        self.__template_index.delete_template(index)
        self.update_tags()

    def add_tag(self):
        """Open a popup window that allows the user to insert values for a new
        template."""
        AddTemplateEditor(self, self.__template_index)


class AddTemplateEditor(PopupWindow):
    """Popup window that allows the user to edit or create a new template."""
    def __init__(self, root, templateIndex, selection = None):
        self._templateIndex = templateIndex
        self._parent = root
        self._selection = selection
        PopupWindow.__init__(self, root)

    def _add_widgets(self):
        """Populate the popup window with widgets."""
       
        top_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)

        # Called in the superclass
        left_frame = tk.Frame(top_frame)
        right_frame = tk.Frame(top_frame)

        tk.Label(left_frame, text="Template name:").pack()
        tk.Label(left_frame, text="Front Tag:").pack()
        tk.Label(left_frame, text="End Tag:").pack()
        tk.Label(left_frame, text="Arguments:").pack()
        
        self.name_entry = tk.Entry(right_frame, width=30)
        self.front_tag_entry = tk.Entry(right_frame, width=30)
        self.end_tag_entry = tk.Entry(right_frame, width=30)
        self.arguments_entry = tk.Entry(right_frame, width=30)
       
        self.name_entry.pack(fill=tk.X, expand=True)
        self.front_tag_entry.pack(fill=tk.X, expand=True)
        self.end_tag_entry.pack(fill=tk.X, expand=True)
        self.arguments_entry.pack(fill=tk.X, expand=True)
       
        top_frame.pack(fill= tk.X, expand=True)
        bottom_frame.pack()

        left_frame.pack(side=tk.LEFT)
        right_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
         
        tk.Button(bottom_frame, text="ok",
                command=self.close).pack()

    def set_defaults(self, name, frontTag, endTag, arguments):
        """Populate the fields of the popup window with the values of the
        currently selected values, for the case that you are editing a
        currently existing template."""
        self.name_entry.insert(0, name)
        self.front_tag_entry.insert(0, frontTag)
        self.end_tag_entry.insert(0, endTag)
        self.arguments_entry.insert(0, " ".join(arguments))
    
    def close(self):
        """Commit the changes made by the user to the data structure, and close
        the window."""

        # Make sure that there are the right amount of arguments to fit the
        # number of '%s' get_string formatting spots in the front tag.
        if len(self.arguments_entry.get().split()) !=\
                self.front_tag_entry.get().count(r"%s"):
            tk.messagebox.showwarning("Argument Error", "The number of"+\
                    " arguments you supplied was not equal to the number of"+\
                    r" '%s' symbols in the front tag.")
            return

        if self._selection == None:
            # Meaning that you are adding a new template
            self._templateIndex.add_template(self.name_entry.get(),
                                             self.front_tag_entry.get(), self.end_tag_entry.get(),
                                             self.arguments_entry.get().split())
        else:
            # Meaning you are editing an existing template
            self._templateIndex.replace_template(self._selection,
                                                 self.name_entry.get(), self.front_tag_entry.get(),
                                                 self.end_tag_entry.get(), self.arguments_entry.get().split())

        self._parent.update_tags()
        self.grab_release()
        self.destroy()


# ------------------ for debugging ---------------------
def __pop():
    top = TemplateEditor(root)


if __name__ == "__main__":
    root = tk.Tk()
    tk.Button(root, text="Pop", command=__pop).pack()
    root.mainloop()

