import gspread
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    items = request.form.getlist('item')
    quantities = request.form.getlist('quantity')
    prices = request.form.getlist('price')
    customer_name = request.form['customer_name']
    customer_address = request.form['customer_address']
    customer_contact = request.form['customer_contact']
    order_list = []
    for i in range(len(items)):
        order_list.append({'item': items[i], 'quantity': quantities[i], 'price': prices[i]})
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Orders").sheet1
    row = [customer_name, customer_address, customer_contact]
    for item in order_list:
        row.append(item['item'])
        row.append(item['quantity'])
        row.append(item['price'])
    sheet.append_row(row)
    return render_template('order.html', order_list=order_list, customer_name=customer_name, customer_address=customer_address, customer_contact=customer_contact)

if __name__ == '__main__':
    app.run(debug=True)
