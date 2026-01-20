// backend/server.js
const express = require('express');
const cors = require('cors');
const db = require('./db'); // DATABASE CONNECTION HERE

const app = express();
app.use(express.json()); 
app.use(cors());         

// MENU ROUTES

// GET: Fetch all menu items (For User Menu View)
app.get('/api/menu', (req, res) => {
    const sql = "SELECT * FROM menuItem";
    db.query(sql, (err, data) => {
        if (err) return res.status(500).json(err);
        return res.json(data);
    });
});

// POST: Add a new menu item (For Admin Dashboard)
app.post('/api/menu', (req, res) => {
    const { name, category, price } = req.body;
    const sql = "SELECT * FROM menuitem";
    const sqlInsert = "INSERT INTO menuitem (`item_name`, `category`, `item_price`) VALUES (?)";
    const values = [name, category, price];

    db.query(sql, [values], (err, result) => {
        if (err) return res.status(500).json(err);
        return res.json({ message: "Menu item added!", id: result.insertId });
    });
});

// BOOKING ROUTES

// POST: Create a new booking (For User Booking Form)
app.post('/api/booking', (req, res) => {
    const { customer_name, date, time, guests } = req.body;
    const sql = "INSERT INTO booking ('booking_id, date, time, guest_count, customer_id, table_id') VALUES (?)";
    const values = [customer_name, date, time, guests];

    db.query(sql, [values], (err, result) => {
        if (err) return res.status(500).json(err);
        return res.json({ message: "Booking successful!", id: result.insertId });
    });
});

// GET: Fetch ALL bookings (For Staff Dashboard)
app.get('/api/bookings', (req, res) => {
    const sql = "SELECT * FROM bookings ORDER BY date, time";
    db.query(sql, (err, data) => {
        if (err) return res.status(500).json(err);
        return res.json(data);
    });
});

// DELETE: Cancel a booking (For Staff Dashboard button)
app.delete('/api/bookings/:id', (req, res) => {
    const sql = "DELETE FROM bookings WHERE id = ?";
    const id = req.params.id;

    db.query(sql, [id], (err, result) => {
        if (err) return res.status(500).json(err);
        return res.json({ message: "Booking deleted." });
    });
});

// Start the server
app.listen(3000, () => {
    console.log("Server is running on port 3000");
});