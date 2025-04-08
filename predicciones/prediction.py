import tensorflow as tf
import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Configuración
IMG_SIZE = (150, 150)
model_path = 'final_model.h5'
UMBRAL_CONFIANZA = 85
LAPIZ_SIZE = {"largo": 15, "ancho": 1, "alto": 1}
CELULAR_SIZE = {"largo": 15, "ancho": 7, "alto": 0.8}

# Cargar modelo
model = tf.keras.models.load_model(model_path)

# Variable global para saber qué objeto fue identificado
objeto_actual = None

def preprocess_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    img = img / 255.0
    return np.expand_dims(img, axis=0)

def predict_image(image):
    img = preprocess_image(image)
    prediction = model.predict(img, verbose=0)[0][0]

    prob_celular = (1 - prediction) * 100
    prob_lapiz = prediction * 100
    max_prob = max(prob_celular, prob_lapiz)

    if max_prob < UMBRAL_CONFIANZA:
        return "NO IDENTIFICADO", max_prob

    label = "CELULAR" if prob_celular > prob_lapiz else "LÁPIZ"
    return label, max_prob

def select_image():
    global objeto_actual

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    try:
        image = cv2.imread(file_path)
        label, confidence = predict_image(image)

        if label == "NO IDENTIFICADO":
            result_label.config(text="No es un celular ni un lápiz", fg="red")
            objeto_actual = None
        else:
            result_label.config(text=f"Objeto reconocido: {label}", fg="green")
            objeto_actual = "celular" if label == "CELULAR" else "lápiz"

        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img_pil)
        image_label.config(image=img_tk)
        image_label.image = img_tk

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar la imagen:\n{str(e)}")

def calcular_cuantos_caben():
    if not objeto_actual:
        messagebox.showwarning("Advertencia", "Primero selecciona una imagen para predecir.")
        return

    try:
        largo = float(entry_largo.get())
        ancho = float(entry_ancho.get())
        alto = float(entry_alto.get())

        if largo <= 0 or ancho <= 0 or alto <= 0:
            messagebox.showwarning("Advertencia", "Las dimensiones deben ser mayores que 0.")
            return

        obj_dims = LAPIZ_SIZE if objeto_actual == "lápiz" else CELULAR_SIZE
        obj_largo, obj_ancho, obj_alto = obj_dims.values()

        total1 = (largo // obj_largo) * (ancho // obj_ancho) * (alto // obj_alto)
        total2 = (largo // obj_ancho) * (ancho // obj_largo) * (alto // obj_alto)
        total3 = (largo // obj_largo) * (ancho // obj_alto) * (alto // obj_ancho)

        total = int(max(total1, total2, total3))

        if objeto_actual == "lápiz":
            resultado_calc.config(text=f"Caben aprox. {total} lápices.")
            return
        else:
            resultado_calc.config(text=f"Caben aprox. {total} celulares.")
            return

    except ValueError:
        messagebox.showerror("Error", "Ingresa números válidos en las dimensiones.")

# Interfaz
root = tk.Tk()
root.title("Prediccion: Celular o Lápiz")

select_button = tk.Button(root, text="Seleccionar Imagen", command=select_image)
select_button.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

result_label = tk.Label(root, text="Resultado aparecerá aquí", font=("Helvetica", 12))
result_label.pack(pady=10)

tk.Label(root, text="Dimensiones de la caja (cm)", font=("Helvetica", 12)).pack(pady=5)
frame_dims = tk.Frame(root)
frame_dims.pack()

tk.Label(frame_dims, text="Largo:").grid(row=0, column=0, padx=5)
entry_largo = tk.Entry(frame_dims)
entry_largo.grid(row=0, column=1)

tk.Label(frame_dims, text="Ancho:").grid(row=1, column=0, padx=5)
entry_ancho = tk.Entry(frame_dims)
entry_ancho.grid(row=1, column=1)

tk.Label(frame_dims, text="Alto:").grid(row=2, column=0, padx=5)
entry_alto = tk.Entry(frame_dims)
entry_alto.grid(row=2, column=1)

btn_calcular = tk.Button(root, text="Calcular cuántos caben", command=calcular_cuantos_caben)
btn_calcular.pack(pady=10)

resultado_calc = tk.Label(root, text="Resultado: ---", font=("Helvetica", 12))
resultado_calc.pack(pady=5)

root.mainloop()