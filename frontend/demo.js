const API_URL = 'http://localhost:3000/api';


// MENU & BOOKING


// Function to Fetch and Display Menu 
async function loadMenu() {
    try {
        const response = await fetch(`${API_URL}/menu`);
        const menuItems = await response.json();
        
        const container = document.getElementById('menu-container');
        container.innerHTML = ''; // Clear "Loading..." text

        menuItems.forEach(item => {
            // Create a card for each menu item
            const card = document.createElement('div');
            card.className = 'menu-item-card'; // This need styling in CSS!!!
            card.innerHTML = `
                <h3>${item.name}</h3>
                <p class="category">${item.category}</p>
                <p class="price">£${item.price}</p>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error loading menu:", error);
        document.getElementById('menu-container').innerHTML = "<p>Failed to load menu.</p>";
    }
}

// Function for Booking Submission 
function setupBookingForm() {
    const form = document.getElementById('booking-form');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Stops page from reloading

        // data from HTML form
        const bookingData = {
            customer_name: document.getElementById('b-name').value,
            date: document.getElementById('b-date').value,
            time: document.getElementById('b-time').value,
            guests: document.getElementById('b-guests').value
        };

        try {
            // send data to Backend
            const response = await fetch(`${API_URL}/booking`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(bookingData)
            });

            const result = await response.json();

            if (response.ok) {
                alert('Booking Confirmed! ID: ' + result.id);
                form.reset(); // Clear the form
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error("Error submitting booking:", error);
            alert("Could not connect to server.");
        }
    });
}

// STAFF & ADMIN


// Function to View All Bookings
async function loadStaffDashboard() {
    const tableBody = document.querySelector('#bookings-table tbody');
    
    try {
        const response = await fetch(`${API_URL}/bookings`); // this route to need to be added to backend!!!
        const bookings = await response.json();

        tableBody.innerHTML = ''; // Clear old rows

        bookings.forEach(booking => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${booking.id}</td>
                <td>${booking.name}</td>
                <td>${new Date(booking.date).toLocaleDateString()}</td>
                <td>${booking.time}</td>
                <td>${booking.guests}</td>
                <td><button onclick="deleteBooking(${booking.id})">Cancel</button></td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading staff dashboard:", error);
    }
}

// Function for Admin to Add Menu Items
function setupAdminMenuForm() {
    const form = document.getElementById('admin-menu-form');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const newItem = {
            name: document.getElementById('m-name').value,
            price: document.getElementById('m-price').value,
            category: document.getElementById('m-category').value
        };

        try {
            await fetch(`${API_URL}/menu`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newItem)
            });
            alert("Menu item added!");
            form.reset();
        } catch (error) {
            alert("Error adding item");
        }
    });
}

// Delete Booking (Optional)
async function deleteBooking(id) {
    if(!confirm("Cancel this booking?")) return;

    await fetch(`${API_URL}/bookings/${id}`, { method: 'DELETE' });
    loadStaffDashboard(); // Refresh table
}