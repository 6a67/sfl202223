flag_enc_path = "flag_enc.jpg"
bit_map_enc_path = "bit_map_enc.jpg"

# read both files
flag_enc_b = open(flag_enc_path, "rb").read()
bit_map_enc_b = open(bit_map_enc_path, "rb").read()

# XOR the two files
flag = bytes([a ^ b for a, b in zip(flag_enc_b, bit_map_enc_b)])

open("flag.jpg", "wb").write(flag)
