import re
import zipfile
from io import BytesIO
import os
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from typing import Literal, Type, Callable, Union
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.module_loading import import_string

def create_zip_file(files: dict, nombre_achivo: str):
    # Open StringIO to grab in-memory ZIP contents
    temp_file = BytesIO()
    # The zip compressor
    zf = zipfile.ZipFile(temp_file, "w")
    for file in files:
        # Calculate path for file in zip
        fdir, fname = os.path.split(files[file].path)
        # zip_path = os.path.join(zip_subdir, fname)
        zip_path = fname
        # Add file, at correct path
        zf.write(files[file].path, zip_path)

    # Must close zip for all contents to be written
    zf.close()
    temp_file.seek(0)
    zip_file = temp_file.read()
    zip_file = SimpleUploadedFile.from_dict({
        'content': zip_file,
        'filename': '{name}.zip'.format(name=nombre_achivo),
        'content-type': 'application/x-zip-compressed'})
    return zip_file


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def decamelize_dict(dictionary: dict) -> dict:
    keys_change: list = []
    for key in dictionary:
        new_key = camel_to_snake(key)
        keys_change.append([key, new_key])
    for key_pair in keys_change:
        dictionary[key_pair[1]] = dictionary.pop(key_pair[0])
    return dictionary


def lista_concatenada(lista: list[str]):
    if len(lista) == 1:
        return lista[0]
    return ', '.join(lista[:-1]) + ' y ' + lista[-1]


def first_name(nombre: str) -> str:
    nombre_requeridor: str = nombre.strip().split(' ')[0]
    return nombre_requeridor.capitalize()


def select_fields(arguments: dict, editable_fields: list[str]) -> dict:
    args = decamelize_dict(json.loads(json.dumps(arguments)))
    new_dict = {}
    for key in args:
        if key in editable_fields:
            new_dict[key] = args[key]
    return new_dict

def get_storage_class(import_path=None):
    return import_string(import_path or settings.DEFAULT_FILE_STORAGE)

def get_storage(storage: Literal['public', 'private'] = 'public') -> Union[Type[Storage], Storage]:
    """
    Returns the appropriate storage class instance based on the provided storage type.

    Args:
        storage: 'public' for default storage, 'private' for private storage.

    Returns:
        An instance of the storage class.
    """
    if storage == 'private':
        storage_class: Type[Storage] = get_storage_class(settings.PRIVATE_FILE_STORAGE)
        return storage_class()
    else:  # 'public'
        return get_storage_class(
            settings.DEFAULT_FILE_STORAGE)()
