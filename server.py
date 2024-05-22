import threading
from socket import *

# Устанавливаем параметры сервера
serverPort = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)

# Подготавливаем сокет сервера
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print('Готов к обслуживанию...')

def handle_client(connectionSocket):
    try:
        # Принимаем сообщение от клиента
        message = connectionSocket.recv(1024).decode()
        
        # Извлекаем имя файла из HTTP-запроса
        filename = message.split()[1]
        f = open(filename[1:])
        
        # Читаем содержимое файла
        outputdata = f.read()
        f.close()
        
        # Отправляем строку HTTP-заголовка
        connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        
        # Отправляем содержимое файла клиенту
        connectionSocket.send(outputdata.encode())
        
        # Закрываем соединение с клиентом
        connectionSocket.close()
    
    except IOError:
        # Отправляем ответ об отсутствии файла на сервере
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'.encode())
        
        # Закрываем клиентский сокет
        connectionSocket.close()

while True:
    # Устанавливаем соединение
    connectionSocket, addr = serverSocket.accept()
    print(f'Соединение установлено с {addr}')
    
    # Создаем новый поток для обработки запроса клиента
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    client_thread.start()

# Закрываем серверный сокет (эта строка никогда не будет выполнена в текущей реализации)
serverSocket.close()
