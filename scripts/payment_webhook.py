from flask import Flask, request
from scripts.warehouse import Warehouse
wh = Warehouse()
app = Flask(__name__)

@app.route('/payment_info', methods=['POST'])
def payment_info():
    data = request.get_json()
    wh.set_payment_webhook(data['options']['user_id'])
    return 'Ok'


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=False)