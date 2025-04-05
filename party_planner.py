#!/usr/bin/env python3
from flask import Flask, request, render_template_string
import sys

app = Flask(__name__)

# Define party items with their values
PARTY_ITEMS = [
    {"index": 0, "name": "Cake", "value": 20},
    {"index": 1, "name": "Balloons", "value": 21},
    {"index": 2, "name": "Music System", "value": 10},
    {"index": 3, "name": "Lights", "value": 5},
    {"index": 4, "name": "Catering Service", "value": 8},
    {"index": 5, "name": "DJ", "value": 3},
    {"index": 6, "name": "Photo Booth", "value": 15},
    {"index": 7, "name": "Tables", "value": 7},
    {"index": 8, "name": "Chairs", "value": 12},
    {"index": 9, "name": "Drinks", "value": 6},
    {"index": 10, "name": "Party Hats", "value": 9},
    {"index": 11, "name": "Streamers", "value": 18},
    {"index": 12, "name": "Invitation Cards", "value": 4},
    {"index": 13, "name": "Party Games", "value": 2},
    {"index": 14, "name": "Cleaning Service", "value": 11}
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Party Planner</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .item-list {
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e9f7ef;
            border-radius: 4px;
        }
        .binary {
            font-family: monospace;
            background-color: #f0f0f0;
            padding: 2px 5px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <h1>Party Planner</h1>
    <h2>Webserver 1</h2>
    <div class="container">
        <h2>Available Party Items:</h2>
        <div class="item-list">
            {% for item in party_items %}
                <div>{{ item.index }}: {{ item.name }}</div>
            {% endfor %}
        </div>
        
        <form method="GET">
            <div class="form-group">
                <label for="indices">Enter item indices separated by commas (e.g., 0, 2):</label>
                <input type="text" id="indices" name="indices" value="{{ request.args.get('indices', '') }}">
            </div>
            <button type="submit">Plan My Party!</button>
        </form>
        
        {% if selected_indices %}
            <div class="result">
                <h3>Your Party Plan:</h3>
                <p><strong>Selected Items:</strong> {{ selected_items_str }}</p>
                
                <p><strong>Base Party Code Calculation:</strong></p>
                <div>
                    {% for item in selected_items %}
                        {{ item.name }} = {{ item.value }} = <span class="binary">{{ item.binary }}</span><br>
                    {% endfor %}
                    {% if selected_items|length > 1 %}
                        {% for i in range(selected_items|length - 1) %}
                            {% if i == 0 %}
                                {{ selected_items[i].value }} & {{ selected_items[i+1].value }} = {{ intermediate_results[i] }}<br>
                            {% else %}
                                {{ intermediate_results[i-1] }} & {{ selected_items[i+1].value }} = {{ intermediate_results[i] }}<br>
                            {% endif %}
                        {% endfor %}
                    {% endif %}
                </div>
                
                <p><strong>Base Party Code:</strong> {{ base_code }}</p>
                
                {% if base_code == 0 %}
                    <p><strong>Adjusted Party Code:</strong> {{ base_code }} + 5 = {{ final_code }}</p>
                {% elif base_code > 5 %}
                    <p><strong>Adjusted Party Code:</strong> {{ base_code }} - 2 = {{ final_code }}</p>
                {% else %}
                    <p><strong>Adjusted Party Code:</strong> {{ base_code }} (unchanged)</p>
                {% endif %}
                
                <p><strong>Final Party Code:</strong> {{ final_code }}</p>
                
                <p><strong>Message:</strong> {{ message }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

def calculate_party_code(selected_indices):
    # Get the selected items
    selected_items = [PARTY_ITEMS[i] for i in selected_indices]
    
    # Calculate the base party code using bitwise AND
    base_code = None
    intermediate_results = []
    
    for item in selected_items:
        if base_code is None:
            base_code = item["value"]
        else:
            base_code &= item["value"]
            intermediate_results.append(base_code)
    
    # If no items were selected, set base_code to 0
    if base_code is None:
        base_code = 0
        
    # Add binary representation to each item
    for item in selected_items:
        item["binary"] = format(item["value"], '05b')
    
    # Apply the conditions to modify the base code
    message = ""
    final_code = base_code
    
    if base_code == 0:
        final_code = base_code + 5
        message = "Epic Party Incoming!"
    elif base_code > 5:
        final_code = base_code - 2
        message = "Let's keep it classy!"
    else:
        message = "Chill vibes only!"
    
    return {
        "selected_items": selected_items,
        "base_code": base_code,
        "final_code": final_code,
        "message": message,
        "intermediate_results": intermediate_results
    }

@app.route('/')
def index():
    selected_indices = []
    result = {}
    selected_items_str = ""
    
    # Get indices from URL parameter
    indices_param = request.args.get('indices', '')
    if indices_param:
        try:
            # Parse and validate indices
            selected_indices = [int(idx.strip()) for idx in indices_param.split(',')]
            selected_indices = [idx for idx in selected_indices if 0 <= idx < len(PARTY_ITEMS)]
            
            # Calculate party code
            result = calculate_party_code(selected_indices)
            
            # Create a string of selected items
            selected_items_str = ", ".join([item["name"] for item in result["selected_items"]])
        except ValueError:
            selected_indices = []
    
    return render_template_string(
        HTML_TEMPLATE,
        party_items=PARTY_ITEMS,
        selected_indices=selected_indices,
        selected_items_str=selected_items_str,
        base_code=result.get("base_code", 0),
        final_code=result.get("final_code", 0),
        message=result.get("message", ""),
        selected_items=result.get("selected_items", []),
        intermediate_results=result.get("intermediate_results", [])
    )

# Command line interface for direct execution
def cli_mode():
    # Display available party items
    print("Webserver 1:")
    print("Available Party Items:")
    
    # Print items with proper formatting
    for item in PARTY_ITEMS:
        print(f"{item['index']}: {item['name']}")
    
    # Get user input
    try:
        input_str = input("\nEnter item indices separated by commas (e.g., 0, 2): ")
        selected_indices = [int(idx.strip()) for idx in input_str.split(',')]
        selected_indices = [idx for idx in selected_indices if 0 <= idx < len(PARTY_ITEMS)]
        if not selected_indices:
            print("No valid indices selected.")
            return
    except ValueError:
        print("Invalid input. Please enter valid indices.")
        return
    
    # Calculate party code
    result = calculate_party_code(selected_indices)
    
    # Display results in the format shown in the screenshot
    print(f"\nSelected Items: {', '.join([item['name'] for item in result['selected_items']])}")
    
    if len(selected_indices) > 1:
        print(f"Base Party Code: {result['selected_items'][0]['value']} & {result['selected_items'][1]['value']} = {result['base_code']}")
    else:
        print(f"Base Party Code: {result['base_code']}")
    
    if result["base_code"] == 0:
        print(f"Adjusted Party Code: {result['base_code']} + 5 = {result['final_code']}")
    elif result["base_code"] > 5:
        print(f"Adjusted Party Code: {result['base_code']} - 2 = {result['final_code']}")
    else:
        print(f"Adjusted Party Code: {result['base_code']} (unchanged)")
    
    print(f"Final Party Code: {result['final_code']}")
    print(f"\nMessage: {result['message']}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_mode()
    elif len(sys.argv) > 1 and sys.argv[1].startswith("--ip="):
        # Extract IP from command line argument
        ip_address = sys.argv[1].split('=')[1]
        app.run(host=ip_address, port=80, debug=False)
    else:
        # For development, bind to localhost
        app.run(debug=True)