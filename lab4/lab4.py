import hashlib
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


# d为b对a的乘法逆
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


# 产生原根
def find_original_root(p):
    for g in range(2, p):  # [2, p-1]
        flag = True
        if quick_pow(g, p - 1, p) != 1:
            continue
        for pi in range(1, p - 1):  # [1, p-2]
            if quick_pow(g, pi, p) == 1:
                flag = False
                break
        if flag:
            return g


# 签名算法
def sign(p, g, m):
    while True:
        k = random.randrange(1, p - 1)  # [1, p-2]
        if euclid(k, p - 1) == 1:
            break
    print("随机产生的k为: ", k)

    t = hashlib.sha256()  # Get the hash algorithm.
    t.update(m.encode("utf-8"))  # Hash the data.
    hm = int(t.hexdigest(), 16)  # Get he hash value.

    r = quick_pow(g, k, p)
    k1 = extend_euclid(p - 1, k)  # k1为k对p-1的乘法逆
    s = (k1 * (hm - x * r)) % (p - 1)

    return m, r, s


# 验证算法
def validate(new_m, r, s, p, g, y):
    t = hashlib.sha256()  # Get the hash algorithm.
    t.update(new_m.encode("utf-8"))  # Hash the data.
    h_new_m = int(t.hexdigest(), 16)  # Get he hash value.

    if (quick_pow(y, r, p) * quick_pow(r, s, p)) % p == quick_pow(g, h_new_m, p):
        return True
    return False


if __name__ == '__main__':

    # 消息
    m = "200110513"

    # 密钥生成
    p = find_large_prime()
    g = find_original_root(p)
    x = random.randrange(2, p)  # [2, p-1]
    y = quick_pow(g, x, p)
    print("公钥(p, g, y) = {}, {}, {}, 私钥x = {}".format(p, g, y, x))

    for i in range(1, 3):
        print("=====第{}次验证=====".format(i))

        # 签名算法
        new_m, r, s = sign(p, g, m)
        print("签名信息: m = {}, (r, s) = ({}, {})".format(new_m, r, s))

        # 验证算法
        if validate(new_m, r, s, p, g, y):
            print("验证成功！")
        else:
            print("验证失败！")

    print("=====消息篡改=====")

    # 签名算法
    new_m, r, s = sign(p, g, m)
    print("签名信息: m = {}, (r, s) = ({}, {})".format(new_m, r, s))

    new_m = "220110513"
    print("消息被篡改为: ", new_m)

    # 验证算法
    if validate(new_m, r, s, p, g, y):
        print("验证成功！")
    else:
        print("验证失败！")
