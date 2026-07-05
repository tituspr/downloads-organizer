import tkinter as tk
from tkinter import ttk
import startup
import threading

window_lock = threading.Lock()


settings_window = None

def open_window():

    global settings_window

    with window_lock:

        if settings_window and settings_window.winfo_exists():
            settings_window.lift()
            settings_window.focus_force()
            return

        settings_window = tk.Tk()


    settings_window.title("Downloads Organizer Settings")
    settings_window.geometry("400x260")
    settings_window.resizable(False, False)

    settings_window.protocol(
        "WM_DELETE_WINDOW",
        close_window
        )


    def save_settings():

        if startup_var.get():
            startup.enable_startup()
        else:
            startup.disable_startup()

        close_window()

    # ---------- Padding ----------
    frame = ttk.Frame(settings_window, padding=20)
    frame.pack(fill="both", expand=True)

    # ---------- Startup ----------
    startup_var = tk.BooleanVar(
        master=settings_window,
        value=startup.is_startup_enabled(),
    )


    ttk.Checkbutton(
        frame,
        text="Start with Windows",
        variable=startup_var,
    ).pack(anchor="w", pady=(0, 10))

    # ---------- Notifications ----------
    notifications_var = tk.BooleanVar(
        master=settings_window,
        value=False,
    )

    ttk.Checkbutton(
        frame,
        text="Enable Notifications",
        variable=notifications_var,
        ).pack(anchor="w", pady=(0, 15))

    # ---------- Delay ----------
    ttk.Label(
        frame,
        text="Organize Delay (seconds)"
    ).pack(anchor="w")

    delay = ttk.Entry(frame, width=8)
    delay.insert(0, "2")
    delay.pack(anchor="w", pady=(5, 20))

    # ---------- Buttons ----------
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x")

    ttk.Button(
        button_frame,
        text="Save",
        command=save_settings,
    ).pack(side="right", padx=5)

    ttk.Button(
        button_frame,
        text="Cancel",
        command=close_window,
    ).pack(side="right")


    settings_window.mainloop()


def close_window():

    global settings_window

    if settings_window and settings_window.winfo_exists():
        settings_window.quit()
        settings_window.destroy()
        settings_window = None


def show():
    if settings_window and settings_window.winfo_exists():
        settings_window.lift()
        settings_window.focus_force()
        return

    threading.Thread(
        target=open_window,
        daemon=True,
    ).start()