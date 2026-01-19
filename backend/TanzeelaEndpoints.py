from flask import Flask, request, jsonify
import sqlalchemy as db

app = Flask(__name__)

db_conn = "mysql+mysqlconnector://root:@localhost:3306/restaurant_database"
engine = db.create_engine(db_conn)


@app.route("/")
def hello_world():
    return jsonify("Hello, World!")

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

@app.route("/api/v1/recipe/<int:item_id>", methods=["GET"])
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

if __name__ == "__main__":
    app.run(debug=True)


