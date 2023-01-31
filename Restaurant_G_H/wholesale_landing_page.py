from flask import Flask, request, render_template
import psycopg2
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        order_id = request.form['order_id']
        items = request.form['items']
        quantity = request.form['quantity']
        totalprice = request.form['totalprice']
        customer_name = request.form['customer_name']
        customer_contact = request.form['customer_contact']
        customer_address = request.form['customer_address']
        delivery_person = request.form['delivery_person']
        status_of_delivery = 'Pending'
        payment_status = request.form['payment_status']

        # Connect to database and update the tables
        conn = psycopg2.connect(database="mydatabase", user="mydatabaseuser", password="mypassword", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute("INSERT INTO orders (order_id, items, quantity, totalprice, customer_name, customer_contact, customer_address, delivery_person, status_of_delivery, payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (order_id, items, quantity, totalprice, customer_name, customer_contact, customer_address, delivery_person, status_of_delivery, payment_status))
        conn.commit()
        cur.close()
        conn.close()

        # Send text message to delivery person
        # Code to send text message goes here

        # Update Google Sheet
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Orders").sheet1
        sheet.append_row([order_id, items, quantity, totalprice, customer_name, customer_contact, customer_address, delivery_person, status_of_delivery, payment_status])

        return 'Order successfully submitted!'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
