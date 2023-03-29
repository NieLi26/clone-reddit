import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image


class ResizingImages:
    def __init__(self) -> None:
        pass

    def resize_image_square(image_path, new_width=250, new_height=250):
        """
        Redimenzionar imagen tipo cuadrada
        """
        # Abrir la imagen original
        with Image.open(image_path) as img:
            # Comprobar las dimensiones originales
            width, height = img.size
            
            # Ajustar las nuevas dimensiones si exceden las dimensiones máximas
            if new_width > width:
                new_width = width
            if new_height > height:
                new_height = height

            # Comprobar si se requiere un nuevo redimensionamiento
            if new_width != width or new_height != height:
                # Redimensionar la imagen
                resized_img = img.resize((new_width, new_height))
            else:
                # No se requiere redimensionamiento
                resized_img = img
            
            # Convertir la imagen al modo de color RGB 
            resized_img = resized_img.convert('RGB')

            # Eliminar la imagen anterior si existe
            # if os.path.exists(image_path):
                # os.remove(image_path)
                # delete image
                    # fs = FileSystemStorage()
                    # fs.delete(image_path)

            # Guardar la imagen redimensionada en el mismo archivo
            resized_img.save(image_path, 'JPEG', quality=90)

    def resize_image_photo(image_path, new_height):
        """
        Redimencionar imagen tipo foto
        """

        # Abrir la imagen original
        with Image.open(image_path) as img:
            # Comprobar las dimensiones originales
            width, height = img.size
            
            # Ajustar las nuevas dimensiones si exceden las dimensiones máximas
            if new_height > height:
                new_height = height

            # Comprobar si se requiere un nuevo redimensionamiento
            if new_height != height:
            # Redimensionar la imagen
                new_width = int(new_height / height * width)
                resized_img = img.resize((new_width, new_height))
            else:
            # No se requiere redimensionamiento
                resized_img = img
            
            # Guardar la imagen redimensionada en el mismo archivo
            resized_img.save(image_path, "JPEG", quality=90)