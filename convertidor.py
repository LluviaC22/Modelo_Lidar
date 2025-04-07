from PIL import Image
import os
import shutil

def convert_images_to_jpg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        try:
            with Image.open(file_path) as img:
                rgb_img = img.convert('RGB')  # Convertir a RGB para evitar errores
                new_filename = os.path.splitext(filename)[0] + ".jpg"
                output_path = os.path.join(output_folder, new_filename)
                rgb_img.save(output_path, "JPEG")
                print(f"Convertido: {filename} -> {new_filename}")
        except Exception as e:
            print(f"No se pudo convertir {filename}: {e}")
    
    shutil.make_archive(output_folder, 'zip', output_folder)
    print(f"Carpeta comprimida en {output_folder}.zip")

# Configuración de carpetas
input_folder = "imagene"  # Cambia esto por la ruta de tu carpeta con imágenes
output_folder = "converted_jpg"

convert_images_to_jpg(input_folder, output_folder)
