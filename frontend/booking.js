let guests = 2;
let selectedTime = null;
let selectedTable = null;

const timeSlots = ["17:00", "18:00", "19:00", "20:00"];


const tables = [
  { id: 201, seats: 2, placement: "Window" },
  { id: 202, seats: 2, placement: "Center" },
  { id: 301, seats: 3, placement: "Center" },
  { id: 401, seats: 4, placement: "Window" },
  { id: 501, seats: 6, placement: "Private" }
];

window.onload = renderTimes;



function changeGuests(change) {
  guests = Math.max(1, Math.min(10, guests + change));
  document.getElementById("guestCount").innerText = guests;
  renderTables();
}



function renderTimes() {
  const grid = document.getElementById("timeGrid");
  grid.innerHTML = "";

  timeSlots.forEach(time => {
    const btn = document.createElement("button");
    btn.innerText = time;
    btn.onclick = () => selectTime(time, btn);
    grid.appendChild(btn);
  });
}

function selectTime(time, btn) {
  selectedTime = time;
  selectedTable = null;

  document.querySelectorAll(".time-grid button")
    .forEach(b => b.classList.remove("active"));

  btn.classList.add("active");
  renderTables();
}



function renderTables() {
  const grid = document.getElementById("tableGrid");
  grid.innerHTML = "";

  if (!selectedTime) {
    grid.innerHTML = "<p>Please select a time.</p>";
    return;
  }

 
  const allowedSeats = [guests, guests + 1];

  const availableTables = tables.filter(t =>
    allowedSeats.includes(t.seats) &&
    !(t.id === 401 && selectedTime === "19:00") 
  );

  if (availableTables.length === 0) {
    grid.innerHTML = "<p>No suitable tables available for this time.</p>";
    return;
  }

  availableTables.forEach(table => {
    const card = document.createElement("div");
    card.className = "table-card";
    card.innerHTML = `
      <strong>Table ${table.id}</strong><br>
      Seats: ${table.seats}<br>
      Location: ${table.placement}
    `;
    card.onclick = () => selectTable(card, table);
    grid.appendChild(card);
  });
}

function selectTable(card, table) {
  selectedTable = table;
  document.querySelectorAll(".table-card")
    .forEach(c => c.classList.remove("active"));
  card.classList.add("active");
}


function confirmBooking() {
  const date = document.getElementById("bookingDate").value;

  if (!date || !selectedTime || !selectedTable) {
    alert("Please complete all booking details.");
    return;
  }

  const booking = {
  date,
  time: selectedTime,
  guest_count: guests,
  table_id: selectedTable.id,
  customer_id: 1
};


  fetch("http://localhost:5000/api/v1/booking", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(booking)
});


  document.getElementById("bookingView").classList.add("hidden");
  document.getElementById("confirmationView").classList.remove("hidden");

  document.getElementById("confirmationText").innerText =
    `Table ${selectedTable.id} for ${guests} guests on ${date} at ${selectedTime}.`;
}
