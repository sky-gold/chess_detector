import random
import string

def generate_random_string(length=10):
    # Создаем строку из всех возможных букв и цифр
    characters = string.ascii_letters + string.digits
    # Генерируем случайную строку заданной длины
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string