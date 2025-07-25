import tkinter as tk
from tkinter import ttk
from AppKit import NSWorkspace, NSImage
from PIL import Image, ImageTk
import psutil
import subprocess
import io

def get_applications_info():
    windows_details = []
    workspace = NSWorkspace.sharedWorkspace()
    # running_apps = workspace.runningApplications()
    launched_apps = workspace.launchedApplications()

    # windows_details = []
    for app_info in launched_apps:
        name = app_info["NSApplicationName"]
        app = app_info["NSWorkspaceApplicationKey"]
        windows_details.append({
            'name': name,
            'bundlePath': app.bundleURL().path(),
            'pid': app.processIdentifier(),
            'icon': app.icon()
        })

    # for app in running_apps:
    #     if app.isActive() and not app.isHidden:
    #         app_info = {
    #             'name': app.localizedName(),
    #             'bundlePath': app.bundleURL().path(),
    #             'pid': app.processIdentifier(),
    #             'icon': app.icon()
    #         }
    #         windows_details.append(app_info)
    
    return windows_details

class AppSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Switcher")
        self.apps_info = get_applications_info()
        self.create_widgets()

    def create_widgets(self):
        self.search_var = tk.StringVar()

        # Create search box
        search_box = ttk.Entry(self.root, textvariable=self.search_var)
        search_box.pack(fill=tk.X, padx=5, pady=5)
        search_box.bind('<KeyRelease>', self.update_app_list)
        search_box.focus_set()

        # Create listbox
        self.tree = ttk.Treeview(self.root, columns=("Icon", "Name"), show="headings")
        self.tree.heading("#1", text="Icon")
        self.tree.heading("#2", text="Name")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.update_app_list()

        # if self.apps_info:
        #     self.tree.selection_set(self.apps_info[0])
        #     self.tree.focus(self.apps_info[0])
        #     self.tree.see(self.apps_info[0])

        self.root.bind('<Return>', self.activate_selected_app)
        self.tree.bind('<Return>', self.activate_selected_app)
        self.root.bind('<Control-n>', self.select_next)
        self.tree.bind('j', self.select_next)
        self.root.bind('<Control-p>', self.select_previous)
        self.tree.bind('k', self.select_previous)

    def nsimage_to_pil(self, nsimage: NSImage) -> Image.Image:
        data = nsimage.TIFFRepresentation()
        if data is None:
            raise ValueError("NSImage has no TIFF representation")
        byte_array = data.bytes()
        pil_image = Image.open(io.BytesIO(byte_array))
        return pil_image

    def update_app_list(self, event=None):
        search_query = self.search_var.get().lower()

        # Clear current entries in the list
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        item_id_list = []
        for app in self.apps_info:
            icon = app['icon']
            name = app['name']
            icon_img = ImageTk.PhotoImage(self.nsimage_to_pil(icon))
            if search_query in name.lower():
                item_id = self.tree.insert('', 'end', image=icon_img, values=(name,))
                self.tree.image = icon_img  # Keep a reference to prevent garbage collection
                item_id_list.append(item_id)

        if item_id_list:
            self.tree.selection_set(item_id_list[0])
            self.tree.focus(item_id_list[0])
            self.tree.see(item_id_list[0])

    def activate_selected_app(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            app_info = self.apps_info[index]
            app_pid = app_info['pid']
            self.activate_app(app_pid)

    def activate_app(self, pid):
        # Activate the app according to its PID
        for app_info in self.apps_info:
            if app_info['pid'] == pid:
                subprocess.run(['open', '-a', app_info['bundlePath']])
                return

    def select_next(self, event):
        selected = self.tree.selection()
        if selected:
            next_item = self.tree.next(selected[0])
            if next_item:
                self.tree.selection_set(next_item)
                self.tree.see(next_item)

    def select_previous(self, event):
        selected = self.tree.selection()
        if selected:
            prev_item = self.tree.prev(selected[0])
            if prev_item:
                self.tree.selection_set(prev_item)
                self.tree.see(prev_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSwitcherApp(root)
    root.mainloop()
