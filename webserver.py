import socket

#HOST,PORT = '127.0.0.1',8082
HOST = ''
PORT = 8082

my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)

print('Listening on port ',PORT)

HTMLOK_HEADER = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
HTML404_HEADER = "HTTP/1.1 404 Not Found\n\n"

def get_html_file(file_name):
    try:
        header = HTMLOK_HEADER

        # open file , r => read , b => byte format
        file = open(file_name,'rb')
        response = file.read()
        file.close()

    except Exception as e:
        header = HTML404_HEADER
        response = '<html><body><h3>Error 404: File not found</h3><p>Python HTTP Server</p></body></html>'.encode('utf-8')
    return (header, response)

while True:
    connection,address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    # Split request from spaces
    string_list = request.split('\n')

    #print(connection, address)
    print("REQUEST:\n", request)

    first_line_list = string_list[0].split(' ')
    #print(first_line_list)
    if len(first_line_list) < 2:
        continue
    method = first_line_list[0]
    requesting_url = first_line_list[1]

    print('Client url request:', requesting_url)

    req_url = requesting_url.split('?')[0] # After the "?" symbol not relevent here
    req_url = req_url.lstrip('/')
    if(req_url == ''):
        header = HTMLOK_HEADER
        response = "<html><h1>You are at Index!</h1></html>"
    elif(req_url == 'hello'):
        header, response = get_html_file("html/hello.html")
    else:
        # if url doesn't match, try to get it as a file
        # or display 404 error
        header, response = get_html_file(req_url)

    final_response = header.encode('utf-8')
    if type(response) == bytes:
        final_response += response
    else:
        final_response += response.encode('utf-8')
    print("RESPONSE:\n", final_response)
    print("----------")
    connection.send(final_response)
    connection.close()
