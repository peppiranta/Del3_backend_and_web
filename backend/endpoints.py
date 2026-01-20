from flask import Flask, request, jsonify
import sqlalchemy as db

app = Flask(__name__)

db_conn = "mysql+mysqlconnector://root:@localhost:3306/restaurant_database"
engine = db.create_engine(db_conn)


@app.route("/")
def hello_world():
    return jsonify("Hello, World!")


# Tanzeela's Endpoints

@app.route("/api/v1/inventoryitem", methods=["GET"])
def get_inventoryitem():
    with engine.connect() as con:
        query = db.text("SELECT * FROM inventoryitem")
        result = con.execute(query).fetchall()
        inventory_list = [dict(row._mapping) for row in result]

        return jsonify(inventory_list)
        
@app.route("/api/v1/inventoryitem", methods=["POST"])
def add_inventoryitem():
    data = request.get_json()

    if not data or "ingredient_name" not in data or "ingredient_quantity" not in data:
        return jsonify({"error message": "could not add inventory item, request body format invalid"})

    with engine.connect() as con:
        query = db.text("""
            INSERT INTO inventoryitem (ingredient_name, ingredient_quantity)
            VALUES (:name, :quantity)
        """)
        con.execute(query, {
            "name": data["ingredient_name"],
            "quantity": data["ingredient_quantity"]
        })
        con.commit()

    return jsonify({"response message": "Inventory item added"})

@app.route("/api/v1/inventoryitem/<int:id>", methods=["GET"])
def get_inventoryitem_by_id(id):
    with engine.connect() as con:
        query = db.text("SELECT * FROM inventoryitem WHERE ingredient_id = :id")
        result = con.execute(query, {"id": id}).fetchone()

    if result is None:
        return jsonify({"error message": "could not find inventory item"})

    return jsonify(dict(result._mapping))

@app.route("/api/v1/inventoryitem/<int:id>", methods=["PUT"])
def update_inventoryitem(id):
    data = request.get_json()

    fields = []
    params = {"id": id}

    if "ingredient_name" in data:
        fields.append("ingredient_name = :name")
        params["name"] = data["ingredient_name"]

    if "ingredient_quantity" in data:
        fields.append("ingredient_quantity = :quantity")
        params["quantity"] = data["ingredient_quantity"]

    if not fields:
        return jsonify({
            "error message": "could not update inventory item, invalid fields"
        })

    with engine.connect() as con:
        query = db.text(f"""
            UPDATE inventoryitem
            SET {", ".join(fields)}
            WHERE ingredient_id = :id
        """)
        result = con.execute(query, params)
        con.commit()

    if result.rowcount == 0:
        return jsonify({
            "error message": "could not find inventory item"
        })

    return jsonify({
        "response message": "Inventory item updated"
    })

@app.route("/api/v1/inventoryitem/<int:id>", methods=["DELETE"])
def delete_inventoryitem(id):
    with engine.connect() as con:
        query = db.text("DELETE FROM inventoryitem WHERE ingredient_id = :id")
        result = con.execute(query, {"id": id})
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "could not find inventory item"})

    return jsonify({"response message": "Inventory item deleted"})


@app.route("/api/v1/menuitem", methods=["GET"])
def get_menuitem():
    with engine.connect() as con:
        query = db.text("SELECT * FROM menuitem")
        result = con.execute(query).fetchall()

    menuitems = [dict(row._mapping) for row in result]

    return jsonify({"menuitem": menuitems})


@app.route("/api/v1/menuitem", methods=["POST"])
def add_menuitem():
    data = request.get_json()

    if not data or "item_name" not in data or "item_price" not in data or "category" not in data:
        return jsonify({
            "error message": "could not add menu item, request body format invalid"
        })

    with engine.connect() as con:
        query = db.text("""
            INSERT INTO menuitem (item_name, item_price, category)
            VALUES (:name, :price, :category)
        """)
        con.execute(query, {
            "name": data["item_name"],
            "price": data["item_price"],
            "category": data["category"]
        })
        con.commit()

    return jsonify({
        "response message": "Menu item added successfully!"
    })


@app.route("/api/v1/menuitem/<int:id>", methods=["GET"])
def get_menuitem_by_id(id):
    with engine.connect() as con:
        query = db.text("SELECT * FROM menuitem WHERE item_id = :id")
        result = con.execute(query, {"id": id}).fetchone()

    if result is None:
        return jsonify({
            "error message": "Could not find menu item."
        })

    return jsonify(dict(result._mapping))


@app.route("/api/v1/menuitem/<int:id>", methods=["PUT"])
def update_menuitem(id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error message": "Could not update menu item, request body format invalid."
        })

    fields = []
    params = {"id": id}

    if "item_name" in data and data["item_name"] != "":
        fields.append("item_name = :name")
        params["name"] = data["item_name"]

    if "item_price" in data and data["item_price"] != "":
        fields.append("item_price = :price")
        params["price"] = data["item_price"]

    if "category" in data and data["category"] != "":
        fields.append("category = :category")
        params["category"] = data["category"]

    if not fields:
        return jsonify({
            "error message": "Could not update menu item, invalid fields."
        })

    with engine.connect() as con:
        query = db.text(f"""
            UPDATE menuitem
            SET {", ".join(fields)}
            WHERE item_id = :id
        """)
        result = con.execute(query, params)
        con.commit()

    if result.rowcount == 0:
        return jsonify({
            "error message": "Could not find menu item."
        })

    return jsonify({
        "response message": "Menu item information updated"
    })


@app.route("/api/v1/menuitem/<int:id>", methods=["DELETE"])
def delete_menuitem(id):
    with engine.connect() as con:
        query = db.text("DELETE FROM menuitem WHERE item_id = :id")
        result = con.execute(query, {"id": id})
        con.commit()

    if result.rowcount == 0:
        return jsonify({
            "error message": "Could not find the menu item"
        })

    return jsonify({
        "response message": "Menu item deleted."
    })

@app.route("/api/v1/recipe", methods=["GET"])
def get_recipe():
    with engine.connect() as con:
        query = db.text("SELECT * FROM recipe")
        result = con.execute(query).fetchall()

    recipe_list = [dict(row._mapping) for row in result]
    return jsonify({"recipe": recipe_list})

@app.route("/api/v1/recipe", methods=["POST"])
def add_recipe():
    data = request.get_json()

    if not data or "item_id" not in data or "recipe" not in data:
        return jsonify({
            "error message": "could not add recipe, request body format invalid"
        })

    with engine.connect() as con:
        # check item exists
        item_check = con.execute(
            db.text("SELECT 1 FROM menuitem WHERE item_id = :id"),
            {"id": data["item_id"]}
        ).fetchone()

        if not item_check:
            return jsonify({
                "error message": "could not find item id"
            })

        for r in data["recipe"]:
            if "ingredient_id" not in r or "used_quantity" not in r:
                return jsonify({
                    "error message": "could not add recipe, request body format invalid"
                })

            # check ingredient exists
            ing_check = con.execute(
                db.text("SELECT 1 FROM inventoryitem WHERE ingredient_id = :id"),
                {"id": r["ingredient_id"]}
            ).fetchone()

            if not ing_check:
                return jsonify({
                    "error message": "could not find ingredient id"
                })

            con.execute(
                db.text("""
                    INSERT INTO recipe (item_id, ingredient_id, used_quantity)
                    VALUES (:item_id, :ingredient_id, :used_quantity)
                """),
                {
                    "item_id": data["item_id"],
                    "ingredient_id": r["ingredient_id"],
                    "used_quantity": r["used_quantity"]
                }
            )

        con.commit()

    return jsonify({"response message": "Recipe added successfully!"})

@app.route("/api/v1/recipe/item/<int:item_id>", methods=["GET"])
def get_recipe_by_item(item_id):
    with engine.connect() as con:
        item_check = con.execute(
            db.text("SELECT 1 FROM menuitem WHERE item_id = :id"),
            {"id": item_id}
        ).fetchone()

        if not item_check:
            return jsonify({"error message": "Could not find menu item"})

        result = con.execute(
            db.text("""
                SELECT ingredient_id, used_quantity
                FROM recipe
                WHERE item_id = :id
            """),
            {"id": item_id}
        ).fetchall()

    if not result:
        return jsonify({"error message": "Could not find recipe for the menu item"})

    ingredients = [dict(row._mapping) for row in result]

    return jsonify({
        "item_id": item_id,
        "ingredients": ingredients
    })

@app.route("/api/v1/recipe/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    data = request.get_json()

    if not data or "used_quantity" not in data or data["used_quantity"] == "":
        return jsonify({
            "error message": "Could not update recipe, invalid fields."
        })

    with engine.connect() as con:
        result = con.execute(
            db.text("""
                UPDATE recipe
                SET used_quantity = :qty
                WHERE recipe_id = :id
            """),
            {
                "qty": data["used_quantity"],
                "id": recipe_id
            }
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "Could not find recipe."})

    return jsonify({"response message": "Recipe information updated"})

@app.route("/api/v1/recipe/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    with engine.connect() as con:
        result = con.execute(
            db.text("DELETE FROM recipe WHERE recipe_id = :id"),
            {"id": recipe_id}
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "Could not find the recipe."})

    return jsonify({"response message": "Recipe deleted."})

@app.route("/api/v1/orderitem", methods=["GET"])
def get_orderitem():
    with engine.connect() as con:
        query = db.text("SELECT * FROM orderitem")
        result = con.execute(query).fetchall()

    orderitem_list = [dict(row._mapping) for row in result]

    return jsonify({"orderitem": orderitem_list})

@app.route("/api/v1/orderitem", methods=["POST"])
def add_orderitem():
    data = request.get_json()

    if not data or not all(k in data for k in
        ("item_quantity", "item_price", "order_id", "item_id")):
        return jsonify({
            "error message": "could not add order item, request body format invalid"
        })

    with engine.connect() as con:
        # optional FK checks (good practice)
        order_check = con.execute(
            db.text("SELECT 1 FROM `order` WHERE order_id = :id"),
            {"id": data["order_id"]}
        ).fetchone()

        item_check = con.execute(
            db.text("SELECT 1 FROM menuitem WHERE item_id = :id"),
            {"id": data["item_id"]}
        ).fetchone()

        if not order_check or not item_check:
            return jsonify({
                "error message": "could not find order id or item id"
            })

        con.execute(
            db.text("""
                INSERT INTO orderitem
                (item_quantity, item_price, order_id, item_id)
                VALUES (:qty, :price, :order_id, :item_id)
            """),
            {
                "qty": data["item_quantity"],
                "price": data["item_price"],
                "order_id": data["order_id"],
                "item_id": data["item_id"]
            }
        )
        con.commit()

    return jsonify({"response message": "Order item added successfully!"})

@app.route("/api/v1/orderitem/<int:id>", methods=["GET"])
def get_orderitem_by_id(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("SELECT * FROM orderitem WHERE order_item_id = :id"),
            {"id": id}
        ).fetchone()

    if result is None:
        return jsonify({"error message": "Could not find the order item."})

    return jsonify(dict(result._mapping))

@app.route("/api/v1/orderitem/<int:id>", methods=["PUT"])
def update_orderitem(id):
    data = request.get_json()

    if not data or "item_quantity" not in data:
        return jsonify({
            "error message": "Could not update order item, invalid fields."
        })

    with engine.connect() as con:
        result = con.execute(
            db.text("""
                UPDATE orderitem
                SET item_quantity = :qty
                WHERE order_item_id = :id
            """),
            {
                "qty": data["item_quantity"],
                "id": id
            }
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "Could not find order item."})

    return jsonify({"response message": "Order item information updated"})

@app.route("/api/v1/orderitem/<int:id>", methods=["DELETE"])
def delete_orderitem(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("DELETE FROM orderitem WHERE order_item_id = :id"),
            {"id": id}
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "Could not find order item."})

    return jsonify({"response message": "Order item deleted."})



# Hammaad's Endpoints

# CUSTOMER
@app.route('/api/v1/customer', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT customer_id, first_name, last_name, email, phone, dietary_preference FROM customer")
    customers = cursor.fetchall()
    conn.close()
    return jsonify({"customer": customers}), 200

@app.route('/api/v1/customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    if not data:
        return jsonify({"error message": "could not add customer, request body format invalid"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO customer (first_name, last_name, email, password, phone, dietary_preference) VALUES (%s,%s,%s,%s,%s,%s)"
    values = (
        data.get('first_name'),
        data.get('last_name'),
        data.get('email'),
        data.get('password'),
        data.get('phone'),
        data.get('dietary_preference')
    )
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Customer added successfully!"}), 201

@app.route('/api/v1/customer/<int:id>', methods=['GET'])
def get_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (id,))
    customer = cursor.fetchone()
    conn.close()

    if not customer:
        return jsonify({"error message": "Could not find customer."}), 404
    return jsonify(customer), 200

@app.route('/api/v1/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    if not data or any(v == "" for v in data.values()):
        return jsonify({"error message": "Could not update customer, invalid fields."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find customer."}), 404

    fields = ", ".join([f"{k}=%s" for k in data.keys()])
    values = list(data.values()) + [id]
    cursor.execute(f"UPDATE customer SET {fields} WHERE customer_id=%s", values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Customer information updated"}), 200

@app.route('/api/v1/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find customer."}), 404

    cursor.execute("DELETE FROM customer WHERE customer_id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"response message": "Customer deleted."}), 200

# Booking
@app.route('/api/v1/booking', methods=['GET'])
def get_bookings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM booking")
    bookings = cursor.fetchall()
    conn.close()
    return jsonify({"booking": bookings}), 200

@app.route('/api/v1/booking', methods=['POST'])
def add_booking():
    data = request.get_json()
    if not data:
        return jsonify({"error message": "could not add booking, request body format invalid"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO booking (date, time, guest_count, customer_id, table_id) VALUES (%s,%s,%s,%s,%s)"
    values = (
        data.get('date'),
        data.get('time'),
        data.get('guest_count'),
        data.get('customer_id'),
        data.get('table_id')
    )
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Booking added successfully!"}), 201

@app.route('/api/v1/booking/<int:id>', methods=['GET'])
def get_booking(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM booking WHERE booking_id=%s", (id,))
    booking = cursor.fetchone()
    conn.close()

    if not booking:
        return jsonify({"error message": "Could not find the booking."}), 404
    return jsonify(booking), 200

@app.route('/api/v1/booking/<int:id>', methods=['PUT'])
def update_booking(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking WHERE booking_id=%s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find booking."}), 404

    fields = ", ".join([f"{k}=%s" for k in data.keys()])
    values = list(data.values()) + [id]
    cursor.execute(f"UPDATE booking SET {fields} WHERE booking_id=%s", values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Booking information updated"}), 200

@app.route('/api/v1/booking/<int:id>', methods=['DELETE'])
def delete_booking(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking WHERE booking_id=%s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find booking."}), 404

    cursor.execute("DELETE FROM booking WHERE booking_id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"response message": "Booking deleted."}), 200

# Table
@app.route('/api/v1/table', methods=['GET'])
def get_tables():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restauranttable")
    tables = cursor.fetchall()
    conn.close()
    return jsonify({"table": tables}), 200

@app.route('/api/v1/table', methods=['POST'])
def add_table():
    data = request.get_json()
    if not data:
        return jsonify({"error message": "could not add table, request body format invalid"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO restauranttable (seats, placement, status) VALUES (%s,%s,%s)"
    values = (data.get('seats'), data.get('placement'), data.get('status'))
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Table added successfully!"}), 201

@app.route('/api/v1/table/<int:id>', methods=['GET'])
def get_table(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restauranttable WHERE table_id=%s", (id,))
    table = cursor.fetchone()
    conn.close()

    if not table:
        return jsonify({"error message": "Could not find the table."}), 404
    return jsonify(table), 200

@app.route('/api/v1/table/<int:id>', methods=['PUT'])
def update_table(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restauranttable WHERE table_id=%s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find table."}), 404

    fields = ", ".join([f"{k}=%s" for k in data.keys()])
    values = list(data.values()) + [id]
    cursor.execute(f"UPDATE restauranttable SET {fields} WHERE table_id=%s", values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Table information updated"}), 200

@app.route('/api/v1/table/<int:id>', methods=['DELETE'])
def delete_table(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restauranttable WHERE table_id=%s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find table."}), 404

    cursor.execute("DELETE FROM restauranttable WHERE table_id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"response message": "Table deleted."}), 200

# order
@app.route('/api/v1/order', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return jsonify({"order": orders}), 200

@app.route('/api/v1/order', methods=['POST'])
def add_order():
    data = request.get_json()
    if not data:
        return jsonify({"error message": "could not add order, request body format invalid"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO orders (order_time, total_amount, customer_id, staff_id, table_id) VALUES (%s,%s,%s,%s,%s)"
    values = (
        data.get('order_time'),
        data.get('total_amount'),
        data.get('customer_id'),
        data.get('staff_id'),
        data.get('table_id')
    )
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Order added successfully!"}), 201

@app.route('/api/v1/order/<int:id>', methods=['GET'])
def get_order(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_id=%s", (id,))
    order = cursor.fetchone()
    conn.close()

    if not order:
        return jsonify({"error message": "Could not find the order."}), 404
    return jsonify(order), 200

@app.route('/api/v1/order/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=%s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find order."}), 404

    fields = ", ".join([f"{k}=%s" for k in data.keys()])
    values = list(data.values()) + [id]
    cursor.execute(f"UPDATE orders SET {fields} WHERE order_id=%s", values)
    conn.commit()
    conn.close()
    return jsonify({"response message": "Order information updated"}), 200

@app.route('/api/v1/order/<int:id>', methods=['DELETE'])
def delete_order(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=%s", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error message": "Could not find order."}), 404

    cursor.execute("DELETE FROM orders WHERE order_id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"response message": "Order deleted."}), 200



# Peppi's Endpoints

# Admin Endpoints

@app.route("/api/v1/admin", methods=["GET"])
def get_admin():
    with engine.connect() as con:
        result = con.execute(db.text("SELECT * FROM admin")).fetchall()
    return jsonify([dict(row._mapping) for row in result])


@app.route("/api/v1/admin", methods=["POST"])
def add_admin():
    data = request.get_json()

    required = ("first_name", "last_name", "position", "email", "password")
    if not data or not all(k in data for k in required):
        return jsonify({"error message": "invalid request body"}), 400

    with engine.connect() as con:
        con.execute(
            db.text("""
                INSERT INTO admin (first_name, last_name, position, email, password)
                VALUES (:first_name, :last_name, :position, :email, :password)
            """),
            data
        )
        con.commit()

    return jsonify({"response message": "Admin added"}), 201


@app.route("/api/v1/admin/<int:id>", methods=["GET"])
def get_admin_by_id(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("SELECT * FROM admin WHERE admin_id = :id"),
            {"id": id}
        ).fetchone()

    if not result:
        return jsonify({"error message": "admin not found"}), 404

    return jsonify(dict(result._mapping))


@app.route("/api/v1/admin/<int:id>", methods=["PUT"])
def update_admin(id):
    data = request.get_json()
    fields, params = [], {"id": id}

    for field in ("first_name", "last_name", "position", "email", "password"):
        if field in data:
            fields.append(f"{field} = :{field}")
            params[field] = data[field]

    if not fields:
        return jsonify({"error message": "invalid fields"}), 400

    with engine.connect() as con:
        result = con.execute(
            db.text(f"UPDATE admin SET {', '.join(fields)} WHERE admin_id = :id"),
            params
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "admin not found"}), 404

    return jsonify({"response message": "Admin updated"})


@app.route("/api/v1/admin/<int:id>", methods=["DELETE"])
def delete_admin(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("DELETE FROM admin WHERE admin_id = :id"),
            {"id": id}
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "admin not found"}), 404

    return jsonify({"response message": "Admin deleted"})




# Staff Endpoints

@app.route("/api/v1/staff", methods=["GET"])
def get_staff():
    with engine.connect() as con:
        result = con.execute(db.text("SELECT * FROM staff")).fetchall()
    return jsonify([dict(row._mapping) for row in result])


@app.route("/api/v1/staff", methods=["POST"])
def add_staff():
    data = request.get_json()

    required = ("first_name", "last_name", "role", "email", "password", "admin_id")
    if not data or not all(k in data for k in required):
        return jsonify({"error message": "invalid request body"}), 400

    with engine.connect() as con:
        admin_id = data.get("admin_id")

        if admin_id is not None:
            admin_check = con.execute(
                db.text("SELECT 1 FROM admin WHERE admin_id = :id"),
                {"id": admin_id}
            ).fetchone()

            if not admin_check:
                return jsonify({
                    "error message": "admin_id does not exist"
                }), 400
        con.execute(
            db.text("""
                INSERT INTO staff (first_name, last_name, role, email, password, admin_id)
                VALUES (:first_name, :last_name, :role, :email, :password, :admin_id)
            """),
            data
        )
        con.commit()

    return jsonify({"response message": "Staff added"}), 201


@app.route("/api/v1/staff/<int:id>", methods=["GET"])
def get_staff_by_id(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("SELECT * FROM staff WHERE staff_id = :id"),
            {"id": id}
        ).fetchone()

    if not result:
        return jsonify({"error message": "staff not found"}), 404

    return jsonify(dict(result._mapping))


@app.route("/api/v1/staff/<int:id>", methods=["PUT"])
def update_staff(id):
    data = request.get_json()
    fields, params = [], {"id": id}

    for field in ("first_name", "last_name", "role", "email", "password", "admin_id"):
        if field in data:
            fields.append(f"{field} = :{field}")
            params[field] = data[field]

    if not fields:
        return jsonify({"error message": "invalid fields"}), 400

    with engine.connect() as con:
        result = con.execute(
            db.text(f"UPDATE staff SET {', '.join(fields)} WHERE staff_id = :id"),
            params
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "staff not found"}), 404

    return jsonify({"response message": "Staff updated"})


@app.route("/api/v1/staff/<int:id>", methods=["DELETE"])
def delete_staff(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("DELETE FROM staff WHERE staff_id = :id"),
            {"id": id}
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "staff not found"}), 404

    return jsonify({"response message": "Staff deleted"})




# Bill Endpoints

@app.route("/api/v1/bill", methods=["GET"])
def get_bill():
    with engine.connect() as con:
        result = con.execute(db.text("SELECT * FROM bill")).fetchall()
    return jsonify([dict(row._mapping) for row in result])


@app.route("/api/v1/bill", methods=["POST"])
def add_bill():
    data = request.get_json()

    required = ("order_id", "total_amount", "payment_method", "paid_by")
    if not data or not all(k in data for k in required):
        return jsonify({"error message": "invalid request body"}), 400

    with engine.connect() as con:
        order_check = con.execute(
            db.text("SELECT 1 FROM orders WHERE order_id = :id"),
            {"id": data["order_id"]}
        ).fetchone()

        if not order_check:
            return jsonify({
                "error message": "order id does not exist"
            }), 404
        con.execute(
            db.text("""
                INSERT INTO bill (order_id, total_amount, payment_method, paid_by)
                VALUES (:order_id, :total_amount, :payment_method, :paid_by)
            """),
            data
        )
        con.commit()

    return jsonify({"response message": "Bill added"}), 201


@app.route("/api/v1/bill/<int:id>", methods=["GET"])
def get_bill_by_id(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("SELECT * FROM bill WHERE bill_id = :id"),
            {"id": id}
        ).fetchone()

    if not result:
        return jsonify({"error message": "bill not found"}), 404

    return jsonify(dict(result._mapping))


@app.route("/api/v1/bill/<int:id>", methods=["PUT"])
def update_bill(id):
    data = request.get_json()
    fields, params = [], {"id": id}

    for field in ("order_id", "total_amount", "payment_method", "paid_by"):
        if field in data:
            fields.append(f"{field} = :{field}")
            params[field] = data[field]

    if not fields:
        return jsonify({"error message": "invalid fields"}), 400

    with engine.connect() as con:
        result = con.execute(
            db.text(f"UPDATE bill SET {', '.join(fields)} WHERE bill_id = :id"),
            params
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "bill not found"}), 404

    return jsonify({"response message": "Bill updated"})


@app.route("/api/v1/bill/<int:id>", methods=["DELETE"])
def delete_bill(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("DELETE FROM bill WHERE bill_id = :id"),
            {"id": id}
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "bill not found"}), 404

    return jsonify({"response message": "Bill deleted"})




# Sales Report Endpoints

@app.route("/api/v1/salesreports", methods=["GET"])
def get_salesreport():
    with engine.connect() as con:
        result = con.execute(db.text("SELECT * FROM salesreports")).fetchall()
    return jsonify([dict(row._mapping) for row in result])


@app.route("/api/v1/salesreports", methods=["POST"])
def add_salesreport():
    data = request.get_json()

    required = ("start_date", "end_date", "total_sales")
    if not data or not all(k in data for k in required):
        return jsonify({"error message": "invalid request body"}), 400

    with engine.connect() as con:
        con.execute(
            db.text("""
                INSERT INTO salesreports (start_date, end_date, total_sales, best_selling, peak_hours)
                VALUES (:start_date, :end_date, :total_sales, :best_selling, :peak_hours)
            """),
            {
                "start_date": data["start_date"],
                "end_date": data["end_date"],
                "total_sales": data["total_sales"],
                "best_selling": data.get("best_selling"),
                "peak_hours": data.get("peak_hours")
            }
        )
        con.commit()

    return jsonify({"response message": "Sales report added"}), 201


@app.route("/api/v1/salesreports/<int:id>", methods=["GET"])
def get_salesreport_by_id(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("SELECT * FROM salesreports WHERE report_id = :id"),
            {"id": id}
        ).fetchone()

    if not result:
        return jsonify({"error message": "sales report not found"}), 404

    return jsonify(dict(result._mapping))


@app.route("/api/v1/salesreports/<int:id>", methods=["PUT"])
def update_salesreport(id):
    data = request.get_json()
    fields, params = [], {"id": id}

    for field in ("start_date", "end_date", "total_sales", "best_selling", "peak_hours"):
        if field in data:
            fields.append(f"{field} = :{field}")
            params[field] = data[field]

    if not fields:
        return jsonify({"error message": "invalid fields"}), 400

    with engine.connect() as con:
        result = con.execute(
            db.text(f"UPDATE salesreports SET {', '.join(fields)} WHERE report_id = :id"),
            params
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "sales report not found"}), 404

    return jsonify({"response message": "Sales report updated"})


@app.route("/api/v1/salesreports/<int:id>", methods=["DELETE"])
def delete_salesreport(id):
    with engine.connect() as con:
        result = con.execute(
            db.text("DELETE FROM salesreports WHERE report_id = :id"),
            {"id": id}
        )
        con.commit()

    if result.rowcount == 0:
        return jsonify({"error message": "sales report not found"}), 404

    return jsonify({"response message": "Sales report deleted"})


if __name__ == '__main__':
    app.run(debug=True)
