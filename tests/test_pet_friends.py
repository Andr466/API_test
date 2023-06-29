from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_add_new_pet_with_valid_data(name='Пёс', animal_type='пес',
                                     age='4'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet(pet_photo='images/fox.jpg'):
    """Проверяем что можно добавить фотографию питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой и фото питомца отстутствует, то добавляем фото питомца
    if len(my_pets['pets']) > 0 and my_pets['pets'][0]['pet_photo'] == '':
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и фото питомца не является пустым значением
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если спиcок питомцев пустой или у питомца имеется фото, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets or pets have photos")


def test_get_api_key_for_invalid_user(email="test111@mail.ru", password='testtesttest'):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_add_new_pet_with_invalid_photo(name='Бобик', animal_type='ретривер',
                                        age='2', pet_photo='123'):
    """Проверяем что нельзя добавить питомца с некорректно введенными данными в фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except:
        raise Exception("Incorrectly added photo")

    # Проверяем, что статус равен 403, так как данные не валидны

    assert status == 403


def test_add_new_pet_with_negative_age(name='Пушок', animal_type='кот',
                                       age='-3'):
    """Проверяем что нельзя добавить питомца c отрицательным значением в поле age"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Ожидаем статус 403, так как данные не валидны
    assert status == 403


def test_add_invalid_photo_of_pet(pet_photo='PHOTO'):
    """Проверяем что возникает ошибка при добавлении некорретных данных в фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем фото питомца
    if len(my_pets['pets']) > 0:
        try:
            status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
            assert status == 403
        except:
            raise Exception("Incorrectly added photo")
    else:
        raise Exception("The list is empty")


def test_get_all_pets_with_invalid_filter(filter='all_pets'):
    """ Проверяем что запрос всех питомцев не возвращает список по
    некорректному значению параметра filter"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200


def test_add_new_pet_with_string_value_in_age(name='Пушок', animal_type='кот',
                                              age='йцукен'):
    """Проверяем что нельзя добавить питомца cо строковым значением в поле age"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Ожидаем статус 403, так как данные не валидны
    assert status == 403


def test_add_text_file_to_pet_photo(pet_photo='images/photo.txt'):
    """Проверяем на добавление текстового файла в раздел фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
    else:
        raise Exception("The list is empty")


def test_add_new_pet_with_integer_value_in_name(name='524', animal_type='кот',
                                                age='3'):
    """Проверяем что нельзя добавить питомца c числовым значением в поле name"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Ожидаем статус 403, так как данные не валидны
    assert status == 403


def test_add_new_pet_with_integer_value_in_animal_type(name='Пушок', animal_type='249',
                                                       age='3'):
    """Проверяем что нельзя добавить питомца c числовым значением в поле animal_type"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Ожидаем статус 403, так как данные не валидны
    assert status == 403
