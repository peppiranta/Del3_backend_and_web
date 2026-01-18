from flask import Flask, request, jsonify
import mysql.connector
app = Flask(__name__)

# Database connection

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='restaurant_database'
    )
 

# Admin Endpoints

@app.route('/api/v1/admin', methods=['GET'])
def get_admins():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT admin_id, first_name, last_name, email FROM admin")
    admins = cursor.fetchall()
    conn.close()
    return jsonify({"admins": admins}), 200

@app.route('/api/v1/admin', methods=['POST'])
def add_admin():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO admin (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
    values = (data.get('first_name'), data.get('last_name'), data.get('email'), data.get('password'))
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"message": "Admin created successfully"}), 201


# Staff Endpoints

@app.route('/api/v1/staff', methods=['GET'])
def get_staff_members():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT staff_id, first_name, last_name, role, phone FROM staff")
    staff = cursor.fetchall()
    conn.close()
    return jsonify({"staff": staff}), 200

@app.route('/api/v1/staff', methods=['POST'])
def add_staff():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO staff (first_name, last_name, role, phone, email) VALUES (%s, %s, %s, %s, %s)"
    values = (data.get('first_name'), data.get('last_name'), data.get('role'), data.get('phone'), data.get('email'))
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"message": "Staff member added"}), 201


# Bill Endpoints

@app.route('/api/v1/bill', methods=['POST'])
def create_bill():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    # This links to order_id and calculates total

    sql = "INSERT INTO bill (order_id, amount, tax, status) VALUES (%s, %s, %s, %s)"
    values = (data.get('order_id'), data.get('amount'), data.get('tax'), data.get('status'))
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"message": "Bill generated"}), 201

@app.route('/api/v1/bill/<int:id>', methods=['GET'])
def get_bill(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bill WHERE bill_id = %s", (id,))
    bill = cursor.fetchone()
    conn.close()
    return jsonify(bill) if bill else (jsonify({"error": "Not found"}), 404)


# Sales Report Endpoints

@app.route('/api/v1/salesreport', methods=['GET'])
def get_sales_reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM salesreport")
    reports = cursor.fetchall()
    conn.close()
    return jsonify({"reports": reports}), 200

@app.route('/api/v1/salesreport/generate', methods=['POST'])
def generate_report():

    # This summarizes all orders for a specific date
    data = request.get_json()
    report_date = data.get('report_date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # This query assumes the report table stores a sum from the orders table
    cursor.execute("""
        INSERT INTO salesreport (report_date, total_revenue, total_orders)
        SELECT %s, SUM(total_amount), COUNT(order_id) FROM orders WHERE DATE(order_time) = %s
    """, (report_date, report_date))
    
    conn.commit()
    conn.close()
    return jsonify({"message": f"Report generated for {report_date}"}), 201