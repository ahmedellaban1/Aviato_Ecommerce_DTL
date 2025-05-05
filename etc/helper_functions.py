import os
from datetime import date
from random import randint


def file_rename(file_name, number_of_digits):
    min_value = 10 ** (number_of_digits - 1)
    max_value = (10 ** number_of_digits) - 1
    _, extension = os.path.splitext(file_name)
    extension = extension.lstrip('.')
    random_number = randint(min_value, max_value)
    formatted_date = date.today().strftime("%m-%Y")
    return f"{random_number}.{extension}", formatted_date


def profile_image_uploader(file, instance):
    file_name, file_date = file_rename(file, 10)
    return f"Profile/{file_date}/{instance.id}-{instance.username}-{file_name}"

