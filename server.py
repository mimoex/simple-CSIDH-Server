from sibc.csidh import CSIDH, default_parameters
import socket

PORT=60006
BUFFER=1024

print("CSIDH server starting...")

csidh = CSIDH(**default_parameters)

# server generates a key
srv_sec_key = csidh.secret_key()
srv_pub_key = csidh.public_key(srv_sec_key)

print("server's publickey: {0}".format(srv_pub_key))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', PORT))
    s.listen(1)
    # クライアントからデータが送られるまで待機
    while True:
        connection, address = s.accept()
        try:
        	#クライアントから公開鍵を受け取る
            cli_pub_key = connection.recv(BUFFER)
            print('Client connected', address)
            print('client-key: ',cli_pub_key)
            
            #クライアントへサーバの公開鍵を送信
            connection.sendall(srv_pub_key)
            
            #共有鍵の生成
            print("Generating SharedKey...")
            shared_secret_srv = csidh.dh(srv_sec_key, cli_pub_key)
            
            #クライアント側で共有鍵が一致するかテスト。送るだけ(Debug)
            connection.sendall(shared_secret_srv)
            print("CSIDH-key: {0}".format(shared_secret_srv))
            
            
        finally:
            connection.close()
