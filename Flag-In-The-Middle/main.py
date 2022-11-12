import socket

HOST = "sfl.cs.tu-dortmund.de"
PORT1 = 10002   # used by Alice
PORT2 = 10003   # used by Bob

public_g = 85   # g, public base
public_p = 1721521895839319678905052879206116244297628155585535737450178608344748052531840924013694224743693    # p, public modulus


def response_decrypt(response_encrypted, key):
    response_int = int.from_bytes(response_encrypted, byteorder='big')
    return str((int(response_int) ^ key).to_bytes(128, byteorder='big'), 'utf-8')


# main function
if __name__ == "__main__":
    socket_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_alice.connect((HOST, PORT1))
    socket_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_bob.connect((HOST, PORT2))

    # get X from Alice
    data = socket_alice.recv(1024)
    X = int(data.decode())
    print(f"Alice->Me: {X}")

    # generate our own secret key
    secret_key = 1234567890

    # calculate our own public key (would make more sense to give both parties a different key)
    public_key = pow(public_g, secret_key, public_p)   # g^secret_key mod p

    # send our public key to Bob
    socket_bob.send(str(public_key).encode())
    print(f"Me->Bob: {public_key}")

    # get Y from Bob
    data = socket_bob.recv(1024)
    Y = int(data.decode())
    print(f"Bob->Me: {Y}")

    # send our public key to Alice
    socket_alice.send(str(public_key).encode())
    print(f"Me->Alice: {public_key}")

    # calculate the shared secret for Alice
    shared_secret_alice = pow(X, secret_key, public_p)   # X^secret_key mod p

    # calculate the shared secret for Bob
    shared_secret_bob = pow(Y, secret_key, public_p)   # Y^secret_key mod p

    # ask Alice for the flag
    socket_alice.send("Flag?".encode())
    print(f"Me->Alice: Flag?")

    # get the flag from Alice
    data = socket_alice.recv(1024)

    # decrypt the flag with the given instructions
    first_part_of_flag = response_decrypt(data, shared_secret_alice)
    print(f"Alice->Me: {first_part_of_flag}")

    # ask Bob for the flag
    socket_bob.send("Flag?".encode())
    print(f"Me->Bob: Flag?")

    # get the flag from Bob
    data = socket_bob.recv(1024)

    # decrypt the flag with the given instructions
    second_part_of_flag = response_decrypt(data, shared_secret_bob)
    print(f"Bob->Me: {second_part_of_flag}")

    # print the flag
    print(f"The flag is:\n{first_part_of_flag}{second_part_of_flag}")

