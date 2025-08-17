import os
from datetime import date
from random import randint
import secrets



def file_rename(file_name, number_of_digits):
    min_value = 10 ** (number_of_digits - 1)
    max_value = (10 ** number_of_digits) - 1
    _, extension = os.path.splitext(file_name)
    extension = extension.lstrip('.')
    random_number = randint(min_value, max_value)
    formatted_date = date.today().strftime("%m-%Y")
    return f"{random_number}.{extension}", formatted_date


def profile_image_uploader(instance, filename):
    file_name, file_date = file_rename(filename, 10)
    return f"Profile/{file_date}/{instance.id}-{instance.user}-{file_name}"


def product_media_uploader(instance, filename):
    file_name, file_date = file_rename(filename, 10)
    return f"Product/{instance.media_type.title()}/{file_date}/{instance.product.id}-{file_name}"


def category_media_uploader(instance, filename):
    file_name, file_date = file_rename(filename, 10)
    return f"Category/{instance.media_type.title()}/{file_date}/{instance.category.id}-{file_name}"


def OTP_random_digits():
    return str(secrets.randbelow(10**6)).zfill(6)
