import math

'''
Use a binary tree to calculate European options (Question 1, Part 1, Part 3)
https://www.wallstreetmojo.com/european-vs-american-option/
My understanding is: American options are more valuable under the same conditions, after all, 
they don’t need to reach a specific point to settle.
I  keep looping and iterating in N times to realize the bifurcation of the binary tree
'''
def EuropeanBSTree(K, T, S, sig, r, N, PorC):
    dt = T / N
    nu = r - 0.5 * sig * sig
    x = math.sqrt(sig * sig * dt + (nu * dt) ** 2)
    dxu = math.exp(x)
    dxd = 1 / dxu
    pu = 0.5 + 0.5 * (nu * dt / x)
    pd = 1 - pu
    disc = math.exp(-r * dt)

    St = [0] * (N + 1)
    C = [0] * (N + 1)

    St[0] = S * dxd ** N

    for j in range(1, N + 1):
        St[j] = St[j - 1] * dxu / dxd

    for j in range(1, N + 1):
        if PorC == "put":
            C[j] = max(K - St[j], 0)
        elif PorC == "call":
            C[j] = max(St[j] - K, 0)

    for i in range(N, 0, -1):
        for j in range(0, i):
            C[j] = disc * (pu * C[j + 1] + pd * C[j])
        print("-" * 10, "\n", C)
    return C[0]

'''
Use a binary tree to calculate American options (Question 1, Part 2, Part 4)
https://www.wallstreetmojo.com/european-vs-american-option/
'''
def AmericanBSTree(K, T, S, sig, r, N, PorC):
    dt = T / N
    dxu = math.exp(sig * math.sqrt(dt))
    dxd = math.exp(-sig * math.sqrt(dt))
    pu = ((math.exp(r * dt)) - dxd) / (dxu - dxd)
    pd = 1 - pu
    disc = math.exp(-r * dt)

    St = [0] * (N + 1)
    C = [0] * (N + 1)

    St[0] = S * dxd ** N

    for j in range(1, N + 1):
        St[j] = St[j - 1] * dxu / dxd

    for j in range(1, N + 1):
        if PorC == "put":
            C[j] = max(K - St[j], 0)
        elif PorC == "call":
            C[j] = max(St[j] - K, 0)

    for i in range(N, 0, -1):
        for j in range(0, i):
            C[j] = disc * (pu * C[j + 1] + pd * C[j])
        print("-" * 10, "\n", C)
    return C[0]


if __name__ == "__main__":
    '''
    Use a binary tree to calculate European and American options (Question 1)
    '''
    price = EuropeanBSTree(60, 10, 70, 0.2, 0.05, 10, "call")
    print("\n EuropeanBSTree call price", format(price, ".2f"))

    price = AmericanBSTree(60, 10, 70, 0.2, 0.05, 10, "call")
    print("\n AmericanBSTree call price", format(price, ".2f"))

    price = EuropeanBSTree(95, 5, 100, 0.1, 0.04, 10, "put")
    print("\n EuropeanBSTree put price", format(price, ".2f"))

    price = AmericanBSTree(95, 5, 100, 0.1, 0.04, 10, "put")
    print("\n AmericanBSTree put price", format(price, ".2f"))

"""
 EuropeanBSTree call price 35.81

 AmericanBSTree call price 36.06

 EuropeanBSTree put price 1.42

 AmericanBSTree put price 1.28
"""
