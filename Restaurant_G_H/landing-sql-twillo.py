from flask import Flask, request, render_template
import sqlite3
from twilio.rest import Client

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
    delivery_person_number = "+1XXXXXXXXXX" # Replace with the delivery person's phone number
    order_list = []
    for i in range(len(items)):
        order_list.append({'item': items[i], 'quantity': quantities[i], 'price': prices[i]})
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS orders (item TEXT, quantity INTEGER, price REAL, customer_name TEXT, customer_address TEXT, customer_contact TEXT)")
    for item in order_list:
        c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", (item['item'], item['quantity'], item['price'], customer_name, customer_address, customer_contact))
    conn.commit()
    conn.close()
    client = Client()
    message = client.messages.create(
        to=delivery_person_number,
        from_="+1XXXXXXXXXX", # Replace with your Twilio number
        body="New order received! Please deliver to {} ({})".format(customer_name, customer_address)
    )
    return render_template('order.html', order_list=order_list, customer_name=customer_name, customer_address=customer_address, customer_contact=customer_contact)

if __name__ == '__main__':
    app.run(debug=True)
