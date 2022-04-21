from sibc.csidh import CSIDH, default_parameters
import socket

PORT=60006

print("Generating CSIDH client key...")

csidh = CSIDH(**default_parameters)

# client generates a key
cli_secret_key = csidh.secret_key()
cli_public_key = csidh.public_key(cli_secret_key)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', PORT))
    s.sendall(cli_public_key)
    srvs_pub_key = s.recv(1024)
    
     #共有鍵の生成
    print("Generating SharedKey...")
    shared_secret_cli = csidh.dh(cli_secret_key, srvs_pub_key)
    
    shared_dh_srv_key = s.recv(1024)
    print(repr(shared_dh_srv_key))
    
    if shared_secret_cli == shared_dh_srv_key:
    	print("OK!")
    else:
    	print("Bad!!!")
    	

# if either alice or bob use their secret key with the other's respective
# public key, the resulting shared secrets are the same
#shared_secret_alice = csidh.dh(alice_secret_key, bob_public_key)
#shared_secret_bob = csidh.dh(bob_secret_key, alice_public_key)

# Alice and bob produce an identical shared secret
#assert shared_secret_alice == shared_secret_bob
