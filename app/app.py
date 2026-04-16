from flask import Flask, render_template, request, redirect, session
from database import init_db, insert_order, get_db_connection
from models import Order
import os

app = Flask(__name__)
app.secret_key = "tcu_bistro_key"

# Initialize DB [cite: 98]
init_db()

@app.route('/')
def index():
    """Step 1: Welcome and Phone Input[cite: 166, 449]."""
    return render_template('index.html')

@app.route('/set_customer', methods=['POST'])
def set_customer():
    """Handles phone validation and returning customer check[cite: 180, 345]."""
    phone = request.form.get('phone')
    # Phone number validation (10 digits) [cite: 346]
    if not (phone.isdigit() and len(phone) == 10):
        return "Invalid phone format. Please use 10 digits.", 400
    
    session['phone'] = phone
    # Identify returning customers [cite: 181]
    conn = get_db_connection()
    user = conn.execute('SELECT name FROM orders WHERE phone = ? ORDER BY id DESC', (phone,)).fetchone()
    conn.close()
    
    session['name'] = user['name'] if user else ""
    return redirect('/customer')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    """Step 2: Customer Name[cite: 185, 468]."""
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        return redirect('/category')
    return render_template('customer.html', name=session.get('name'))

@app.route('/category', methods=['GET', 'POST'])
def category():
    """Step 3: Select Sandwich or Wrap[cite: 202, 476]."""
    if request.method == 'POST':
        session['category'] = request.form.get('category')
        return redirect('/build')
    return render_template('category.html')

@app.route('/build')
def build():
    """Step 4: Build Order[cite: 221, 494]."""
    # Using list and loop for toppings 
    topping_list = ["Lettuce", "Tomato", "Onion", "Pickles", "Spinach"]
    return render_template('build.html', toppings=topping_list)

@app.route('/submit', methods=['POST'])
def submit():
    """Process order and save to DB[cite: 521, 541]."""
    my_order = Order(session['category'], request.form.get('size'), request.form.get('protein'))
    toppings = request.form.getlist('toppings')
    
    # String manipulation for details 
    details_str = f"Size: {my_order.size}, Protein: {my_order.protein}, Toppings: {', '.join(toppings)}"
    
    total = my_order.calculate_total(len(toppings))
    
    order_data = {
        'phone': session['phone'],
        'name': session['name'],
        'cat': session['category'],
        'details': details_str,
        'total': total
    }
    
    insert_order(order_data)
    return render_template('confirm.html')

if __name__ == '__main__':
    app.run(debug=True)
