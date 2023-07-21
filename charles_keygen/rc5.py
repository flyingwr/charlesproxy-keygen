def twos_comp(num, bits=32):
    return num - (1 << bits) if num & (1 << (bits - 1)) else num

def rotate_left(x, n, bits=32):
    return ((x << (n % bits)) | (x >> (bits - (n % bits)))) & (1 << bits) - 1

def rotate_right(x, n, bits=32):
    return ((x >> (n % bits)) | (x << (bits - (n % bits)))) & (1 << bits) - 1

class RC5:
    def __init__(self):
        self.r = 12
        self.t = 26
        self.s = [0] * self.t
        self.p = 0xB7E15163
        self.q = 0x9E3779B9

    def encrypt(self, pt, ct):
        a, b = (pt[0] + self.s[0]), (pt[1] + self.s[1])

        for i in range(1, self.r + 1):
            a = rotate_left((a ^ b) & 0xffffffff, b) + self.s[2 * i]
            b = rotate_left((b ^ a) & 0xffffffff, a) + self.s[2 * i + 1]

        ct[0], ct[1] = twos_comp(a), twos_comp(b)

    def decrypt(self, ct, pt):
        b, a = ct[1], ct[0]

        for i in range(self.r, 0, -1):
            b = rotate_right((b - self.s[2 * i + 1] & 0xffffffff), a) ^ a
            a = rotate_right((a - self.s[2 * i]) & 0xffffffff, b) ^ b

        pt[1], pt[0] = b - self.s[1], a - self.s[0]

    def schedule(self, w, h):
        L = [w, h]

        self.s[0] = self.p
        for i in range(1, self.t):
            self.s[i] = self.s[i - 1] + self.q

        a = b = i = j = 0
        for _ in range(3 * self.t):
            a = self.s[i] = twos_comp(rotate_left((self.s[i] + a + b) & 0xffffffff, 3))
            b = L[j] = twos_comp(rotate_left((L[j] + a + b) & 0xffffffff, a + b))
            i, j = (i + 1) % self.t, (j + 1) % 2

    def encrypt_block(self, block):
        array = [0] * len(block)
        n = len(block)

        n2 = j = k = l = 0
        for i in range(n):
            if j < 4:
                l <<= 8
                l |= block[i] & 0xFF
            else:
                k <<= 8
                k |= block[i] & 0xFF
            j += 1

            if n2 == 7:
                pt = [k, l]
                ct = [0, 0]
                self.encrypt(pt, ct)

                array[i - 7] = twos_comp((ct[1] >> 24) & 0xff, 8)
                array[i - 6] = twos_comp((ct[1] >> 16) & 0xff, 8)
                array[i - 5] = twos_comp((ct[1] >> 8) & 0xff, 8)
                array[i - 4] = twos_comp(ct[1] & 0xff, 8)
                array[i - 3] = twos_comp((ct[0] >> 24) & 0xff, 8)
                array[i - 2] = twos_comp((ct[0] >> 16) & 0xff, 8)
                array[i - 1] = twos_comp((ct[0] >> 8) & 0xff, 8)
                array[i] = twos_comp(ct[0] & 0xff, 8)

                n2 = j = k = l = 0
            else:
                n2 += 1

        return array
