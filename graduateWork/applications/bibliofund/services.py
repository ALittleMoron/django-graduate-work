import os


def custom_upload_to(instance, filename):
    """ Кастомная функция для создания пути к загруженному файлу.
    
    Формат для Document: 'documents/user_{username}/filename'
    """
    folder = f'{instance.__class__.__name__.lower()}s'
    user_folder = f'user_{instance.publisher.get_username()}'
    return os.path.join(folder, user_folder, filename)
