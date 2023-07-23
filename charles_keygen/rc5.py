def rotate_left(x, n, bits=32):
    return ((x << (n % bits)) | (x >> (bits - (n % bits)))) & (1 << bits) - 1

def rotate_right(x, n, bits=32):
    return ((x >> (n % bits)) | (x << (bits - (n % bits)))) & (1 << bits) - 1

class RC5: # 32-bit
    def __init__(self):
        self.r = 12
        self.t = 26
        self.s = [0] * self.t
        self.p = 0xb7e15163
        self.q = 0x9e3779b9

    def encrypt(self, pt, ct):
        a, b = (pt[0] + self.s[0]), (pt[1] + self.s[1])

        for i in range(1, self.r + 1):
            a = rotate_left((a ^ b) & 0xffffffff, b) + self.s[2 * i]
            b = rotate_left((b ^ a) & 0xffffffff, a) + self.s[2 * i + 1]

        ct[0], ct[1] = a, b

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
            a = self.s[i] = rotate_left((self.s[i] + a + b) & 0xffffffff, 3)
            b = L[j] = rotate_left((L[j] + a + b) & 0xffffffff, a + b)
            i, j = (i + 1) % self.t, (j + 1) % 2

    def encrypt_block(self, block):
        array = [0] * len(block)
        n = len(block)

        l = k = 0
        for i in range(n):
            if i % 8 < 4:
                l = (l << 8) | (block[i] & 0xff)
            else:
                k = (k << 8) | (block[i] & 0xff)
            
            if i % 8 == 7:
                pt = [k, l]
                ct = [0, 0]
                self.encrypt(pt, ct)

                for j in range(7, -1, -1):
                    array[i - j] = (ct[j // 4] >> ((j % 4) * 8)) & 0xff

                l = k = 0

        return array

    def decrypt_block(self, block):
        array = [0] * len(block)
        n = len(block)

        l = k = 0
        for i in range(n):
            if i % 8 < 4:
                l = (l << 8) | (block[i] & 0xff)
            else:
                k = (k << 8) | (block[i] & 0xff)
            
            if i % 8 == 7:
                ct = [k, l]
                pt = [0, 0]
                self.decrypt(ct, pt)

                for j in range(7, -1, -1):
                    array[i - j] = (pt[j // 4] >> ((j % 4) * 8)) & 0xff

                l = k = 0

        return array