from flask import Flask, request, jsonify

from calculations import Calculations

app = Flask(__name__)


@app.route('/calc_fee', methods=['POST'])
def calc_delivery_fee():
    request_data = request.get_json()
    fee = Calculations().get_delivery_fee(request_data['cart_value'], request_data['delivery_distance'],
                                          request_data['number_of_items'], request_data['time'])
    response = {'delivery_fee': fee}

    return jsonify(response)


if __name__ == "__main__":
    app.run()
