import socket
import sys

def http_client(server_host, server_port, filename):
    # Создаем TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Подключаемся к серверу
    client_socket.connect((server_host, int(server_port)))
    
    # Формируем HTTP-запрос
    request_line = f"GET /{filename} HTTP/1.1\r\n"
    headers = f"Host: {server_host}:{server_port}\r\n"
    headers += "Connection: close\r\n\r\n"
    http_request = request_line + headers
    
    # Отправляем HTTP-запрос на сервер
    client_socket.sendall(http_request.encode())
    
    # Получаем ответ от сервера
    response = ""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data.decode()
    
    # Закрываем сокет
    client_socket.close()
    
    # Выводим ответ сервера
    print(response)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: client.py <server_host> <server_port> <filename>")
        sys.exit(1)
    
    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]
    
    http_client(server_host, server_port, filename)
