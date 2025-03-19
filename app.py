from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="sqldatabasepassword", 
    database="billing_db"
)
cursor = db.cursor()

# Route to Display Billing Form
@app.route('/')
def index():
    return render_template('index.html')

# Route to Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    contact = request.form['contact']
    items = request.form['items']
    total_amount = request.form['total_amount']

    # Check if customer exists
    cursor.execute("SELECT id FROM customers WHERE contact=%s", (contact,))
    customer = cursor.fetchone()

    if customer:
        customer_id = customer[0]
    else:
        cursor.execute("INSERT INTO customers (name, contact) VALUES (%s, %s)", (name, contact))
        db.commit()
        customer_id = cursor.lastrowid

    # Insert bill
    cursor.execute("INSERT INTO bills (customer_id, items, total_amount) VALUES (%s, %s, %s)",
                   (customer_id, items, total_amount))
    db.commit()

    return redirect('/bills')

# Route to Retrieve and Display Bills
@app.route('/bills')
def bills():
    cursor.execute("""SELECT b.id, c.name, c.contact, b.items, b.total_amount, b.bill_date 
                      FROM bills b 
                      JOIN customers c ON b.customer_id = c.id""")
    bills_data = cursor.fetchall()
    return render_template('bills.html', bills=bills_data)

if __name__ == '__main__':
    app.run(debug=True)
