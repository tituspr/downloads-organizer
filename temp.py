# import startup
# import time

# print(startup.is_startup_enabled())
# print(startup.get_startup_folder())
# print(startup.get_shortcut_path())

# startup.enable_startup()

# time.sleep(10)

# print(startup.is_startup_enabled())

# startup.disable_startup()

# print(startup.is_startup_enabled())

import tkinter as tk
import settings

root = tk.Tk()
root.withdraw()

settings.open_window(root)

root.mainloop()