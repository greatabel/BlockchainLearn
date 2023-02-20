from ecdsa import SigningKey, SECP256k1
import random

# 假设我们要证明知道私钥k的值，但不想直接将k的值传递给验证方
# 首先，我们使用椭圆曲线加密生成一个公钥和一个私钥
sk = SigningKey.generate(curve=SECP256k1)
pk = sk.verifying_key

# 下面是证明阶段的代码，用于生成证明
# 随机选择一个比特b
b = random.randint(0, 1)

# 如果b=0，我们将发送私钥k的值给验证方
# 如果b=1，我们将发送公钥pk的值给验证方
if b == 0:
    proof = sk.to_string()
else:
    proof = pk.to_string()

# 验证阶段的代码，用于验证证明
# 随机选择一个比特b
b = random.randint(0, 1)

# 如果b=0，我们将接受私钥k，并验证它是否可以用于签名
# 如果b=1，我们将接受公钥pk，并验证它是否可以用于验证签名
if b == 0:
    msg = b"Hello, world!"
    sig = sk.sign(msg)
    result = pk.verify(sig, msg)
else:
    msg = b"Hello, world!"
    sig = pk.sign(msg, sk)
    result = sk.verifies(sig, msg)

if result:
    print("Verification succeeded")
else:
    print("Verification failed")
