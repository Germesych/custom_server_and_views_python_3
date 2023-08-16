import socket
from views import *


URLS = {
    '/': index,
    '/blog': blog,
}


# Обработка запроса клиента
def parse_request(request):
    # Разбиваем строку по пробелу
    parsed = request.split(' ')
    # получаем метод GET, POST, DELETE, PUT...
    method = parsed[0]
    # Получаем url
    url = parsed[1]
    return (method, url)


# Генерация ошибок и обработка url
def generate_headers(method, url):
    if not method == 'GET':
        return ("HTTP/1.1 405 Method not allowed!\n\n", 405)

    if not url in URLS:
        return ('HTTP/1.1 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


# Генерация тела ответа
def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found!</p>'

    if code == 405:
        return '<h1>404</h1><p>Method not allowed!</p>'

    # Вызываем функцию нашего представления
    return URLS[url]()


# Ответ пользователю
def generate_response(request):
    # Распаковываем метод и url
    method, url = parse_request(request)
    # Получение заголовков и ответа:
    headers, code = generate_headers(method, url)
    # Тело ответа
    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    # Параметры IP-4 и TSP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Задать сокету право отключаться без таймаута в 1-4 минуты
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # На каком адресе и порте работать
    server_socket.bind(('localhost', 5050))
    # Прослушать порт
    server_socket.listen()
    
    # Клиентская часть
    while True:
        # Тут то что сервер принял 1) какой сокет нам что-то отправил. 2 Адрес сокета который к нам подключился
        client_socket, addr = server_socket.accept()
        # Это данные от клиента в байт представлении
        request = client_socket.recv(1024)
        print(f"request: {request.decode('utf-8')}")
        print()
        print(f"Client Address: {addr}")

        # Ответ клиенту чем либо
        response = generate_response(request.decode('utf-8'))

        # Ответ клиенту который прислал нам данные закодированный в байт строку
        # client_socket.sendall('Hello world'.encode())
        client_socket.sendall(response)
        # Закрыли соединение после ответа
        client_socket.close()


if __name__ == '__main__':
    run()
