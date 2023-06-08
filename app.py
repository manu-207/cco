from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host='cco-db.czj7jypmn3wk.us-east-1.rds.amazonaws.com',
    user='admin',
    password='Manu5718',
    database='manu_db'
)

# Function to calculate the price difference
def calculate_price_difference(intel_price, graviton_price):
    return intel_price - graviton_price

# Function to get the low-cost instance suggestion
def get_lowcost_instance(intel_price, graviton_price):
    if intel_price < graviton_price:
        return "Intel"
    elif graviton_price < intel_price:
        return "Graviton"
    else:
        return "Both instances have the same price."

# Function to compare the instances and get the results
def compare_instances(vcpu_size):
    cursor = db.cursor()

    # Query the Intel table to get the price and RAM size based on vCPU size
    query_intel = "SELECT instance_type, `price`, RAM FROM intel WHERE vCPU = %s"
    cursor.execute(query_intel, (vcpu_size,))
    intel_result = cursor.fetchone()
    intel_instance, intel_price, intel_ram = intel_result[0], intel_result[1], intel_result[2]

    # Query the Graviton table to get the price and RAM size based on vCPU size
    query_graviton = "SELECT instance_type, `price`, RAM FROM graviton WHERE vCPU = %s"
    cursor.execute(query_graviton, (vcpu_size,))
    graviton_result = cursor.fetchone()
    graviton_instance, graviton_price, graviton_ram = graviton_result[0], graviton_result[1], graviton_result[2]

    # Calculate the price difference
    price_difference = calculate_price_difference(intel_price, graviton_price)

    # Get the low-cost instance suggestion
    lowcost_instance = get_lowcost_instance(intel_price, graviton_price)

    cursor.close()

    # Render the template with the results
    return render_template('results.html', intel_instance=intel_instance, intel_price=intel_price, intel_ram=intel_ram, graviton_instance=graviton_instance, graviton_price=graviton_price, graviton_ram=graviton_ram, price_difference=price_difference, lowcost_instance=lowcost_instance)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vcpu_size = request.form['vcpu']
        return compare_instances(vcpu_size)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
