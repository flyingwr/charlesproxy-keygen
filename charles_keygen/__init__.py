from .rc5 import rotate_left, RC5

import struct

def generate_key(name):
    def xor_checksum(n):
        n2 = 0
        for i in range(56, -1, -8):
            n2 ^= (n >> i) & 0xff
        return n2

    def name_checksum(name):
        size = len(name)

        name_array = bytearray(4) + name.encode()
        name_array += bytes(8 - len(name_array) % 8)
        name_array[0], name_array[1], name_array[2], name_array[3] = size >> 24 & 0xff, size >> 16 & 0xff, size >> 8 & 0xff, size & 0xff

        r = RC5()
        r.schedule(1763497072, 2049034577)
        output_array = r.encrypt_block(name_array)

        n = 0
        for by in output_array:
            n ^= struct.unpack("b", struct.pack("B", by))[0] # get signed
            n = rotate_left(n & 0xffffffff, 3)
        return n

    license_key_checksum = 1418211210
    license_name_checksum_val = name_checksum(name)
    license_key_checksum ^= license_name_checksum_val
    b_license_key = license_key_checksum
    b_license_key <<= 32
    b_license_key |= 0x1cad6bc

    key_enc = [b_license_key & 0xffffffff, b_license_key >> 32]
    key_dec = [0, 0]

    r = RC5()
    r.schedule(3960385453, 3035685068)
    r.decrypt(key_enc, key_dec)

    key_decrypted = ((key_dec[1] & 0xffffffff) << 32) | key_dec[0] & 0xffffffff

    xor_checksum_val = xor_checksum(b_license_key)
    return f"{xor_checksum_val:02X}{key_decrypted:016X}"