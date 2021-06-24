import math


# math erf implementation
def my_fnor_func(x):
    y = 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return y

'''
 Black-Scholes- Merton model
 Please see the specific principle introduction：

 https://www.youtube.com/watch?v=JxFvz94uBOY
 https://www.youtube.com/watch?v=sbdba4AB5JM
'''
def Black_Scholes(t, St, K, T, r, sig, PorC):
    Tmt = T - t
    ATmt = sig * math.sqrt(Tmt)
    logo = math.log(St / K)
    Ap = (logo + (r + 0.5 * sig ** 2) * Tmt) / ATmt
    An = Ap - ATmt

    if PorC == "call":
        p = St * my_fnor_func(Ap) - K * math.exp(-r * Tmt) * my_fnor_func(An)
    elif PorC == "put":
        p = K * math.exp(-r * Tmt) * my_fnor_func(-An) - St * my_fnor_func(-Ap)
    return p


if __name__ == "__main__":
    '''
    Call the formula to calculate European options (Question 2)
    '''
    price = Black_Scholes(0, 70, 60, 10, 0.05, 0.2, "call")
    print(
        "1. European call option (S0 = 70, K = 60, T = 10, r = 0.05, σ = 0.2, N = 10)"
    )
    print("Black Scholes call price", format(price, ".2f"))

    price = Black_Scholes(0, 100, 95, 5, 0.04, 0.1, "put")
    print("3. European put option (S0 = 100, K = 95, T = 5, r = 0.04, σ = 0.1, N = 10)")
    print("Black Scholes put price", format(price, ".2f"))

"""
output
1. European call option (S0 = 70, K = 60, T = 10, r = 0.05, σ = 0.2, N = 10)
Black Scholes call price 36.02
3. European put option (S0 = 100, K = 95, T = 5, r = 0.04, σ = 0.1, N = 10)
Black Scholes put price 1.29

"""
