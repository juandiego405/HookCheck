from tkinter import *
from tkinter import font  # Importa el módulo font
import cv2
from PIL import Image, ImageTk
import threading

class CameraApp:
    def __init__(self, window):
        self.window = window
        window.geometry("1100x700")
        window.configure(bg = "#4f6b96")
        self.exit_flag = False
        self.lock = threading.Lock()  # Lock para detener los hilos

        self.canvas = Canvas(
            window,
            bg = "#4f6b96",
            height=700,
            width=1100,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        self.label_camera = Label(window)
        self.label_camera.place(x=90, y=168)

        self.label_roi = Label(window)
        self.label_roi.place(x=560, y=168)

        background_img = PhotoImage(file="C:\\Users\\juand\\OneDrive\\Documentos\\Universidad\\10 semestre\\vision artificial\\TrabajoFinal\\TrabajoFinal\\GUI\\background.png")

        self.background = self.canvas.create_image(550.0, 350, image=background_img)

        img0 = PhotoImage(file="C:\\Users\\juand\\OneDrive\\Documentos\\Universidad\\10 semestre\\vision artificial\\TrabajoFinal\\TrabajoFinal\\GUI\\img0.png")
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_inicio,
            relief="flat"
        )

        b0.place(
            x = 860, y = 447,
            width = 173,
            height = 38)

        img1 = PhotoImage(file="C:\\Users\\juand\\OneDrive\\Documentos\\Universidad\\10 semestre\\vision artificial\\TrabajoFinal\\TrabajoFinal\\GUI\\img1.png")
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_Parar,
            relief="flat"
        )

        b1.place(
            x = 860, y = 529,
            width = 173,
            height = 38)

        # OptionMenu dentro del frame

        window.resizable(False, False)

        self.start_threads()
        self.selected_pieza = StringVar()
        self.selected_pieza.set("Seleccionar pieza") 
        pieza_options = ["Pieza1", "Pieza2", "Pieza3", "Pieza4", "Pieza5"]
        self.pieza_menu = OptionMenu(self.canvas, self.selected_pieza, *pieza_options)

        # Configura la fuente para el menú desplegable
        font_style = font.Font(family="Book Antiqua", size=12)
        self.pieza_menu['font'] = font_style
        self.pieza_menu.configure(font=font_style, bg="#A6A06D")

        self.pieza_menu.place(x=860, y=300)

        window.protocol("WM_DELETE_WINDOW", self.stop_threads)
        window.mainloop()


    def btn_inicio(self):
        print("Boton inicio")
    
    def btn_Parar(self):
        print("Boton parar")

    def roi(self, frame, x, y, width, height):
        return frame[y:y+height, x:x+width]

    def update_camera_frame(self):
        while not self.exit_flag:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (350, 230))
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)
                self.label_camera.config(image=img)
                self.label_camera.image = img

    def update_roi_frame(self):
        while not self.exit_flag:
            ret, frame = self.cap.read()
            if ret:
                roiImage = self.roi(frame=frame, x=0, y=0, width=220, height=220)
                roiImage = cv2.resize(roiImage, (240, 230))
                img = cv2.cvtColor(roiImage, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)
                self.label_roi.config(image=img)
                self.label_roi.image = img

    def start_threads(self):
        self.exit_flag = False
        self.camera_thread = threading.Thread(target=self.update_camera_frame)
        self.roi_thread = threading.Thread(target=self.update_roi_frame)

        self.camera_thread.daemon = True
        self.roi_thread.daemon = True

        self.camera_thread.start()
        self.roi_thread.start()

    def stop_threads(self):
        self.exit_flag = True
        self.cap.release()
        self.lock.acquire()  # Adquiere el bloqueo
        self.window.destroy()  # Destruye la ventana
        self.lock.release()  # Libera el bloqueo

if __name__ == "__main__":
    root = Tk()
    app = CameraApp(root)
    root.mainloop()
