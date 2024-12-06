from flask import Flask, render_template_string, request
import csv
from collections import deque
from datetime import datetime
app = Flask(__name__)
index = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ticket Management</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&display=swap" rel="stylesheet">
<style>
body{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    justify-content: center;
    align-items: center;
    margin: 0;
    font-size: 20px;
}

div{
    border: 2px solid #800080;
    border-radius: 8px;
    padding: 15px;
    width: 1000px;
}

.josefin-sans-normal{
    font-family: "Josefin Sans", serif;
    font-optical-sizing: auto;
    font-weight: 350;
    font-style: normal;
  }

.josefin-sans-bold{
    font-family: "Josefin Sans", serif;
    font-optical-sizing: auto;
    font-weight: 600;
    font-style: normal;
  }
  

h1, h2, h3, h4{
    text-align: center;
}

#forms{
    text-align: center;
    margin: 0 auto;
}

#name{
    border: 1px solid #DEDEDF;
    width: 180px;
    height: 25px;
    outline: none;
    padding: 10px;
    border-radius: 5px;
    font-size: 20px;
}

#delete_name{
    border: 1px solid #DEDEDF;
    width: 180px;
    height: 25px;
    outline: none;
    padding: 10px;
    border-radius: 5px;
    font-size: 20px;
}

#delete_type{
    border: 1px solid #DEDEDF;
    outline: none;
    width: 180px;
    height: 43px;
    border-radius: 5px;
    padding: 10px;
    font-size: 18px;
}

#buttons{
    width: 200px;
    height: 30px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background-color: #800080;
    color: #ffffff;
}

#buttons:hover{
    background-color: transparent;
    color: #800080;
    border: 2px solid #800080;
}

#deleteButton{
    width: 200px;
    height: 30px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background-color: red;
    color: white;
}

#deleteButton:hover{
    background-color: rgba(255, 0, 0, 0.121);
    background-color: transparent;
    color: red;
    border: 2px solid red;
}

span{
    display: block;
    width: 100%;
    margin: 20px 0;
    background-color: #800080;
    border-radius: 2px;
    height: 2px;
}

ul{
    list-style: none;
    padding: 0;
    text-align: center;
    margin: 0 auto;
}

ul li{
    padding: 5px;
}

p{
    text-align: center;
    margin: 0 auto;
    padding: 10px;
}
</style>
</head>
<body>
<div>
<h1 class="josefin-sans-bold">Ticket Management System</h1>

    
    <h2 class="josefin-sans-bold">Add Ticket</h2>
    <form action="/add_ticket" method="POST" id="forms" class="josefin-sans-normal">
        <label for="ticket_type" class="josefin-sans-bold">Ticket Type:</label>
        <input type="radio" id="vip" name="ticket_type" value="vip"> VIP
        <input type="radio" id="regular" name="ticket_type" value="regular"> Regular
        <br><br>
        <label for="name" class="josefin-sans-bold">Name:</label>
        <input type="text" id="name" name="name"class="josefin-sans-normal" required>
        <br><br>
        <button type="submit" class="josefin-sans-normal" id="buttons">Add Ticket</button>
    </form>

    <span></span>

    <h2 class="josefin-sans-bold">Delete Ticket</h2>
    <form action="/delete_ticket" method="POST" class="josefin-sans-normal" id="forms">
        <label for="delete_name" class="josefin-sans-bold">Name:</label>
        <input type="text" id="delete_name" name="delete_name" class="josefin-sans-normal" required>
        <br><br>
        <label for="delete_type" class="josefin-sans-bold">Ticket Type:</label>
        <select name="delete_type" id="delete_type" class="josefin-sans-normal">
            <option value="vip">VIP</option>
            <option value="regular">Regular</option>
        </select>
        <br><br>
        <button type="submit" class="josefin-sans-normal" id="deleteButton">Delete Ticket</button>
    </form>

    <span></span>

    <h2 class="josefin-sans-bold">Process Tickets</h2>
    <form action="/process" method="POST" class="josefin-sans-normal" id="forms">
        <button type="submit" class="josefin-sans-normal" id="buttons">Process All Tickets</button>
    </form>

    {% if message %}
        <p class="josefin-sans-normal">{{ message }}</p>
    {% endif %}

    {% if ticket_summary %}
        <h3 class="josefin-sans-bold">Ticket Summary:</h3>
        <p class="josefin-sans-normal">VIP Tickets Sold: {{ ticket_summary.vip_sold }}</p>
        <p class="josefin-sans-normal">VIP Tickets Available: {{ ticket_summary.vip_available }}</p>
        <p class="josefin-sans-normal">Regular Tickets Sold: {{ ticket_summary.regular_sold }}</p>
        <p class="josefin-sans-normal">Regular Tickets Available: {{ ticket_summary.regular_available }}</p>
    {% endif %}

    <h3 class="josefin-sans-bold">Current Tickets:</h3>
    <h4 class="josefin-sans-bold">VIP Tickets:</h4>
    <ul class="josefin-sans-normal">
        {% for ticket in vip_tickets %}
            <li>{{ ticket[0] }} (VIP) - Added on: {{ ticket[2] }}</li>
        {% else %}
            <li>No VIP tickets.</li>
        {% endfor %}
    </ul>

    <h4 class="josefin-sans-bold">Regular Tickets:</h4>
    <ul class="josefin-sans-normal">
        {% for ticket in regular_tickets %}
            <li>{{ ticket[0] }} (Regular) - Added on: {{ ticket[2] }}</li>
        {% else %}
            <li>No regular tickets.</li>
        {% endfor %}
    </ul>
</div> 
</body>
</html>
"""
# Initialize ticket queues and counts
vip = deque()
regular = deque()
vip_og = vip_available = 5
reg_og = regular_available = 15

# Home route for displaying the form
@app.route('/')
def home():
    return render_template_string(
        index, 
        vip_available=vip_available, 
        regular_available=regular_available,
        vip_tickets=vip, 
        regular_tickets=regular
    )

# Route to handle adding tickets
@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    global vip_available, regular_available

    ticket_type = request.form.get('ticket_type')
    name = request.form.get('name').title().strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp

    if ticket_type == 'vip' and vip_available > 0:
        vip.append((name, 'vip', timestamp))  # Store ticket with timestamp
        vip_available -= 1
        message = f"VIP ticket for {name} added successfully."
    elif ticket_type == 'regular' and regular_available > 0:
        regular.append((name, 'regular', timestamp))  # Store ticket with timestamp
        regular_available -= 1
        message = f"Regular ticket for {name} added successfully."
    else:
        message = "No tickets available of that type."

    return render_template_string(
        index, 
        vip_available=vip_available, 
        regular_available=regular_available, 
        vip_tickets=vip, 
        regular_tickets=regular, 
        message=message
    )

# Route to handle deleting tickets
@app.route('/delete_ticket', methods=['POST'])
def delete_ticket():
    global vip_available, regular_available

    name = request.form.get('delete_name').title().strip()
    ticket_type = request.form.get('delete_type')

    # Check and remove the ticket from the appropriate queue
    if ticket_type == 'vip':
        for ticket in list(vip):  # Using list to create a copy to prevent runtime errors during removal
            if ticket[0] == name:
                vip.remove(ticket)
                vip_available += 1
                message = f"Ticket for {ticket[0]} (VIP) deleted successfully."
                break
        else:
            message = "VIP ticket not found."
    elif ticket_type == 'regular':
        for ticket in list(regular):
            if ticket[0] == name:
                regular.remove(ticket)
                regular_available += 1
                message = f"Ticket for {ticket[0]} (Regular) deleted successfully."
                break
        else:
            message = "Regular ticket not found."
    else:
        message = "Ticket type not found."

    return render_template_string(
        index, 
        vip_available=vip_available, 
        regular_available=regular_available, 
        vip_tickets=vip, 
        regular_tickets=regular, 
        message=message
    )
    
# Route to process the tickets
@app.route('/process', methods=['POST'])
def process():
    global vip_available, regular_available

    with open('tickets.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Type', 'Transaction Success', 'Timestamp'])  # Added Timestamp column

        # Process VIP tickets
        while vip:
            name, type, timestamp = vip.popleft()
            writer.writerow([name, 'vip', 'Success', timestamp])  # Write timestamp to the CSV

        # Process Regular tickets
        while regular:
            name, type, timestamp = regular.popleft()
            writer.writerow([name, 'regular', 'Success', timestamp])  # Write timestamp to the CSV

    # After processing, reset the ticket counts
    ticket_summary = {
        'vip_sold': vip_og - vip_available,
        'vip_available': vip_available,
        'regular_sold': reg_og - regular_available,
        'regular_available': regular_available
    }
    # Reset the variables
    vip_available = vip_og
    regular_available = reg_og
    return render_template_string(
        index, 
        ticket_summary=ticket_summary,
        vip_available=vip_available,
        regular_available=regular_available,
        vip_tickets=vip,
        regular_tickets=regular
    )

app.run(debug=True)
