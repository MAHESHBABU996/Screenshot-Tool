import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import os
import threading
from PIL import ImageGrab
import keyboard
import pyperclip
import datetime

# ---------------- SETUP ----------------
BASE_DIR = "E:/Projects/Python/screenshots"
os.makedirs(BASE_DIR, exist_ok=True)


def get_folder():
    folder = os.path.join(BASE_DIR, datetime.date.today().isoformat())
    os.makedirs(folder, exist_ok=True)
    return folder


def generate_name():
    return f"snap_{time.strftime('%H-%M-%S')}.png"


# ---------------- MAIN APP ----------------
class ProSnippingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Snipping Tool")
        self.root.geometry("360x420")
        self.root.resizable(False, False)

        self.history = []

        # UI STYLE
        style = ttk.Style()
        style.theme_use("clam")

        title = tk.Label(root, text="🔥 Pro Snipping Tool", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        ttk.Button(root, text="📸 Full Screenshot", command=self.full_screenshot).pack(pady=5)
        ttk.Button(root, text="✂ Snip Area", command=self.snip_area).pack(pady=5)
        ttk.Button(root, text="📁 Open History", command=self.show_history).pack(pady=5)
        ttk.Button(root, text="❌ Exit", command=root.destroy).pack(pady=5)

        self.status = tk.Label(root, text="", fg="green")
        self.status.pack(pady=10)

        # HOTKEY
        threading.Thread(target=self.hotkey_listener, daemon=True).start()

    # ---------------- HOTKEY ----------------
    def hotkey_listener(self):
        keyboard.add_hotkey("ctrl+shift+s", self.snip_area)
        keyboard.wait()

    # ---------------- NOTIFY ----------------
    def notify(self, text):
        self.status.config(text=text)
        self.root.after(2000, lambda: self.status.config(text=""))

    # ---------------- CLIPBOARD ----------------
    def copy_to_clipboard(self, img):
        temp = os.path.join(BASE_DIR, "temp.png")
        img.save(temp)
        pyperclip.copy(temp)

    # ---------------- FULL SCREEN ----------------
    def full_screenshot(self):
        self.root.withdraw()
        time.sleep(0.3)

        folder = get_folder()
        path = os.path.join(folder, generate_name())

        img = ImageGrab.grab()
        img.save(path)

        pyperclip.copy(path)
        os.startfile(path)

        self.history.append(path)

        self.root.deiconify()
        self.notify("Full screenshot saved ✔")

    # ---------------- SNIP MODE ----------------
    def snip_area(self):
        self.root.withdraw()
        time.sleep(0.2)

        self.snip = tk.Toplevel()
        self.snip.attributes("-fullscreen", True)
        self.snip.attributes("-alpha", 0.25)
        self.snip.attributes("-topmost", True)
        self.snip.configure(bg="black")

        self.canvas = tk.Canvas(self.snip, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.start)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def start(self, e):
        self.x1, self.y1 = e.x, e.y
        self.rect = self.canvas.create_rectangle(self.x1, self.y1, self.x1, self.y1, outline="red", width=2)

    def drag(self, e):
        self.canvas.coords(self.rect, self.x1, self.y1, e.x, e.y)

    def release(self, e):
        x2, y2 = e.x, e.y
        self.snip.destroy()

        x1, y1 = min(self.x1, x2), min(self.y1, y2)
        x2, y2 = max(self.x1, x2), max(self.y1, y2)

        if abs(x2 - x1) < 5 or abs(y2 - y1) < 5:
            self.root.deiconify()
            return

        folder = get_folder()
        path = os.path.join(folder, generate_name())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save(path)

        pyperclip.copy(path)
        os.startfile(path)

        self.history.append(path)

        self.root.deiconify()
        self.notify("Snip saved ✔ copied ✔")

    # ---------------- HISTORY ----------------
    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("History")
        win.geometry("400x300")

        for p in reversed(self.history):
            btn = ttk.Button(win, text=p, command=lambda x=p: os.startfile(x))
            btn.pack(fill="x", padx=5, pady=2)


# ---------------- RUN ----------------
root = tk.Tk()
app = ProSnippingApp(root)
root.mainloop()