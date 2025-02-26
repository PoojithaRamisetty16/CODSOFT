import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

video_capture = None
is_camera_running = False

def detect_faces_image():
    global image
    global canvas


    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


    file_path = filedialog.askopenfilename()

    if file_path:
    
        image = cv2.imread(file_path)
        image = cv2.resize(image, (340, 380))

    
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        
        num_faces = len(faces)

        
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

    
        canvas.config(image=image_tk)
        canvas.image = image_tk

        
        if num_faces > 0:
            result_label.config(text=f'Faces Detected: {num_faces}', fg="#000", bg="#d6cadd")
        else:
            result_label.config(text="No faces detected", fg="#990000", bg="#d6cadd")


def detect_faces_camera():
    global video_capture
    global is_camera_running

    if not is_camera_running:
        
        video_capture = cv2.VideoCapture(0)
        video_capture.set(3, 320)  # Width
        video_capture.set(4, 240)  # Height

        
        is_camera_running = True

        
        detect_faces()

    else:
        messagebox.showinfo("Info", "Camera is already running.")


def stop_camera():
    global video_capture
    global is_camera_running

    if video_capture is not None:
        video_capture.release()

    is_camera_running = False
    result_label.config(text="Camera stopped.", fg="#990000", bg="#d6cadd")
    canvas.config(image='')


def clear_image():
    global canvas
    result_label.config(text='', fg="#333333", bg="#f0f0f0")
    canvas.config(image='')


def detect_faces():
    global image
    global canvas
    global video_capture
    global root

    if video_capture is not None:
        ret, frame = video_capture.read()

        if ret:
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        
            num_faces = len(faces)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(frame_pil)

            canvas.config(image=frame_tk)
            canvas.image = frame_tk

        
            result_text = f'Faces Detected: {num_faces}\n'
            for i, (x, y, w, h) in enumerate(faces):
                result_text += f'Face {i + 1}: (X:{x}, Y:{y}, W:{w}, H:{h})\n'

            result_label.config(text=result_text, fg="#990000", bg="#d6cadd")

        
            root.after(10, detect_faces)

root = tk.Tk()
root.title("Face Detection GUI")
root.geometry("800x700")
root.configure(bg="#f0f0f0")  

title_label = tk.Label(root, text="          Face Detection          ", font=("Arial", 40), fg="#333333", bg="#ffd700")
title_label.pack(pady=20)

button_style = tk.Button(root, text="Open Image", command=detect_faces_image, font=("Arial", 16), fg="white", bg="#007acc", padx=10, pady=5)
button_style.pack(pady=10)

camera_button = tk.Button(root, text="Camera Detection", command=detect_faces_camera, font=("Arial", 16), fg="white", bg="#007acc", padx=10, pady=5)
camera_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Camera", command=stop_camera, font=("Arial", 16), fg="white", bg="#d32f2f", padx=10, pady=5)
stop_button.pack(pady=10)

clear_button = tk.Button(root, text="Clear Image", command=clear_image, font=("Arial", 16), fg="white", bg="#28a745", padx=10, pady=5)
clear_button.pack(pady=10)

canvas = tk.Label(root, bg="#f0f0f0")
canvas.pack()
result_label = tk.Label(root, text='', font=('Arial', 22), fg="#333333", bg="#f0f0f0", padx=10, pady=5)
result_label.pack()
root.mainloop()
