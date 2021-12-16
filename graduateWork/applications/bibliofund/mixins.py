from typing import Optional

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Document


class UserIsPublisher(UserPassesTestMixin):
    """ Класс проверки принадлежности пользователя к посту с картинкой. """
    def get_image(self):
        """ Метод, возвращающий инстанс документа по id. """
        return get_object_or_404(Document, slug=self.kwargs.get('slug'))

    def test_func(self) -> Optional[bool]:
        """ Метод, проверяющий пользователя на авторство в посте с картинкой.  """
        if self.request.user.is_authenticated:
            return self.request.user == self.get_image().publisher
        else:
            raise PermissionDenied('Извините, у вас нет доступа к этому разделу')