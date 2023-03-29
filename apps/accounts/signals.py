# import os
# from django.core.files.storage import FileSystemStorage
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import CustomUser


# @receiver(pre_save, sender=CustomUser)
# def users_thumbnail_pre_delete(sender, instance, **kwargs):
#     image = instance.thumbnail.path

#     # Check if the image exists
#     if os.path.exists(image):
#         # delete image
#         fs = FileSystemStorage()
#         fs.delete(image)
#     else:
#         print('Imagen no existe')
