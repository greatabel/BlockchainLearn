from Crypto.PublicKey import RSA
from termcolor import colored


def show(s,color='green'):
    print(colored(s, color, attrs=['reverse', 'blink']))

key = RSA.generate(2048)

pv_key_string = key.exportKey()


with open("d3private.pem", "w") as prv_file:
    print("{}".format(pv_key_string.decode()), file=prv_file)

pb_key_string = key.publickey().exportKey()
with open("d3public.pem", "w") as pub_file:
    print("{}".format(pb_key_string.decode()), file=pub_file)

print('pv_key_string = ', pv_key_string)
show('-'*30)
print('pb_key_string = ', pb_key_string)