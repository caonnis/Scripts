import pyautogui
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from PIL import Image, ImageDraw
from screeninfo import get_monitors

class ScreenCapture:
    def __init__(self):
        self.monitor = None
        self.root = tk.Tk()
        self.select_monitor()

    def select_monitor(self):
        self.root.title("Selecciona un Monitor")
        self.root.geometry("300x200")

        monitor_list = get_monitors()
        tk.Label(self.root, text="Selecciona el monitor:").pack(pady=10)

        for idx, monitor in enumerate(monitor_list):
            tk.Button(self.root, text=f"Monitor {idx + 1}: {monitor.width}x{monitor.height}", 
                      command=lambda m=monitor: self.set_monitor(m)).pack(pady=5)

        self.root.mainloop()

    def set_monitor(self, monitor):
        self.monitor = monitor
        self.root.destroy()
        self.init_capture()

    def init_capture(self):
        self.capture_root = tk.Tk()
        self.capture_root.geometry(f"{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}")
        self.capture_root.attributes('-fullscreen', True)
        self.capture_root.attributes('-alpha', 0.3)
        self.capture_root.configure(background='grey')

        self.canvas = tk.Canvas(self.capture_root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.current_rectangle = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.capture_root.bind("<Escape>", lambda e: self.capture_root.quit())

        self.capture_screen()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if not self.current_rectangle:
            self.current_rectangle = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, 
                outline='red', width=2
            )

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.current_rectangle, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.capture_root.quit()

    def capture_screen(self):
        self.capture_root.mainloop()

        if self.current_rectangle:
            x1, y1, x2, y2 = map(int, self.canvas.coords(self.current_rectangle))
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            screenshot = pyautogui.screenshot(region=(self.monitor.x + x1, self.monitor.y + y1, x2 - x1, y2 - y1))
            highlighted = Image.new('RGBA', screenshot.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(highlighted)
            draw.rectangle([0, 0, x2 - x1, y2 - y1], outline='red', width=2)

            result = Image.alpha_composite(screenshot.convert('RGBA'), highlighted)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile=filename
            )

            if save_path:
                result.save(save_path)
                print(f"Captura de pantalla guardada como: {save_path}")
            else:
                print("Captura de pantalla cancelada.")

if __name__ == "__main__":
    ScreenCapture()
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageDraw
from screeninfo import get_monitors

class ScreenCapture:
    def __init__(self):
        self.monitor = None
        self.root = tk.Tk()
        self.select_monitor()

    def select_monitor(self):
        self.root.title("Selecciona un Monitor")
        self.root.geometry("300x200")

        monitor_list = get_monitors()
        tk.Label(self.root, text="Selecciona el monitor:").pack(pady=10)

        for idx, monitor in enumerate(monitor_list):
            tk.Button(self.root, text=f"Monitor {idx + 1}: {monitor.width}x{monitor.height}", 
                      command=lambda m=monitor: self.set_monitor(m)).pack(pady=5)

        self.root.mainloop()

    def set_monitor(self, monitor):
        self.monitor = monitor
        self.root.destroy()
        self.init_capture()

    def init_capture(self):
        self.capture_root = tk.Tk()
        self.capture_root.geometry(f"{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}")
        self.capture_root.attributes('-fullscreen', True)
        self.capture_root.attributes('-alpha', 0.3)
        self.capture_root.configure(background='grey')

        self.canvas = tk.Canvas(self.capture_root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.current_rectangle = None

        self.toolbar = tk.Frame(self.capture_root, bg='white')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.capture_btn = tk.Button(self.toolbar, text="Capturar", command=self.save_capture)
        self.capture_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.cancel_btn = tk.Button(self.toolbar, text="Cancelar", command=self.capture_root.quit)
        self.cancel_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.capture_root.bind("<Escape>", lambda e: self.capture_root.quit())

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if not self.current_rectangle:
            self.current_rectangle = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, 
                outline='red', width=2
            )

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.current_rectangle, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        pass

    def save_capture(self):
        if self.current_rectangle:
            x1, y1, x2, y2 = map(int, self.canvas.coords(self.current_rectangle))
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            screenshot = pyautogui.screenshot(region=(self.monitor.x + x1, self.monitor.y + y1, x2 - x1, y2 - y1))
            highlighted = Image.new('RGBA', screenshot.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(highlighted)
            draw.rectangle([0, 0, x2 - x1, y2 - y1], outline='red', width=2)

            result = Image.alpha_composite(screenshot.convert('RGBA'), highlighted)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile=filename
            )

            if save_path:
                result.save(save_path)
                messagebox.showinfo("Captura de Pantalla", f"Captura de pantalla guardada como: {save_path}")
            else:
                messagebox.showwarning("Captura de Pantalla", "Captura de pantalla cancelada.")

            self.capture_root.quit()

if __name__ == "__main__":
    ScreenCapture()
