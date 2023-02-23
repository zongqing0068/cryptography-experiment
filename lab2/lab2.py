import random


# mod n下的快速幂算法
# m为底数，e为指数，计算m**e%n
def quick_pow(m, e, n):
    ans = 1
    while e:
        if e & 1:
            ans = (ans * m) % n
        m = m * m % n
        e >>= 1
    return ans


# 对prime进行素性检测
def is_prime(prime):
    k = 0
    q = prime - 1
    while not q % 2:
        q >>= 1
        k += 1
    assert prime - 1 == (1 << k) * q

    a = random.randrange(2, prime)  # 2到prime-1之间的随机整数
    remain = quick_pow(a, q, prime)
    if remain == 1 or remain == prime - 1:
        return True  # 很有可能为素数

    for i in range(1, k):
        if quick_pow(a, ((1 << i) * q), prime) == prime - 1:
            return True  # 很有可能为素数

    return False  # 为合数


# 产生一个大素数
def find_large_prime():
    while True:
        prime = random.randrange(100001, 1000000, 2)  # 生成随机大奇数
        if is_prime(prime):
            return prime


# 欧几里得算法求最大公因数
def euclid(a, b):
    x = a
    y = b
    while y != 0:
        r = x % y
        x = y
        y = r
    return x


# 产生公钥e
# e与fai_n互质
def find_e(fai_n):
    while True:
        e = random.randrange(2, fai_n)
        if euclid(e, fai_n) == 1:
            return e


# 产生私钥d
# d为b对a的乘法逆，即e对fai_n的乘法逆
def extend_euclid(a, b):
    x = [1, 0, a]
    y = [0, 1, b]
    t = [0, 0, 0]
    while y[2] != 1:
        q = x[2] // y[2]
        for i in range(3):
            t[i] = x[i] - q * y[i]
        x[:] = y[:]
        y[:] = t[:]
    d = (y[1] + a) % a
    return d


# 删去空格和其他标点符号
def plaintext_reprocess(plain_text):
    new_text = []
    for item in plain_text:
        if '0' <= item <= '9' or 'a' <= item <= 'z' or 'A' <= item <= 'Z':
            new_text.append(item)
    return new_text


# 将文本转化为数字
def text2num(text):
    text_num = []
    for item in text:
        if '0' <= item <= '9':
            text_num.append(int(item))
        elif 'a' <= item <= 'z':
            text_num.append(10 + ord(item) - ord('a'))
        elif 'A' <= item <= 'Z':
            text_num.append(36 + ord(item) - ord('A'))
    return text_num


# 将数字转化为文本
def num2text(text_num):
    for ids, item in enumerate(text_num):
        if 0 <= item <= 9:
            text_num[ids] = chr(ord('0') + item)
        elif 10 <= item <= 35:
            text_num[ids] = chr(ord('a') + item - 10)
        elif 36 <= item <= 61:
            text_num[ids] = chr(ord('A') + item - 36)
        else:
            del text_num[ids]  # 删去填充位
    return text_num


# 加密
def encryption(plain_text_num, e, n):
    i = 0
    cipher_text_num = []  # 密文分组
    while i < len(plain_text_num):
        if i == len(plain_text_num) - 1:  # 对不足四位的进行填充
            plain_text_num.append(62)
        plain_num = plain_text_num[i] * 100 + plain_text_num[i + 1]
        cipher_num = quick_pow(plain_num, e, n)
        cipher_text_num.append(cipher_num)
        i += 2
    return cipher_text_num


# 解密
def decryption(cipher_text_num, d, n):
    plain_text_num = []  # 明文
    for item in cipher_text_num:
        plain_num = quick_pow(item, d, n)
        plain_text_num.append(plain_num // 100)
        plain_text_num.append(plain_num % 100)
    return plain_text_num


if __name__ == '__main__':
    p = find_large_prime()
    q = find_large_prime()
    n = p * q
    fai_n = (p - 1) * (q - 1)
    e = find_e(fai_n)
    d = extend_euclid(fai_n, e)
    with open("./lab2-Plaintext.txt", "r") as file:
        plain_text = file.read()
    new_plain_text = plaintext_reprocess(plain_text)
    plain_text_num = text2num(new_plain_text)
    cipher_text_num = encryption(plain_text_num, e, n)
    dec_plain_text_num = decryption(cipher_text_num, d, n)
    dec_plain_text = num2text(dec_plain_text_num)

    # 原明文与解密后的明文相同
    assert ''.join(new_plain_text) == ''.join(dec_plain_text)

    print("p = ", p, "\nq = ", q, "\nn = ", n, "\ne = ", e, "\n𝜙(𝑛) = ", fai_n)
    print("加密后的密文为：", cipher_text_num)
    print("解密后的明文为：", ''.join(dec_plain_text))

