from flask import Flask, request
from flask import render_template
import sqlite3
import socket, pickle
import sys,random
sys.path.append('/Users/abel/AbelProject/BlockchainLearn/b18488_SecureMPartyComputation')



app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@app.route('/demo', methods=['GET', 'POST'])
def search():
    # --------- share data -------
    r = 'no_finished'
    try:
        fp = open("shared.pkl", "rb")
        shared = pickle.load(fp)
        r = shared["flag"]
        print('app back thread is receving:', r)
    except:
        print("An exception occurred")
    # --------- share data end -------
    return render_template('search.html', r=r)

if __name__ == '__main__':
    app.run()