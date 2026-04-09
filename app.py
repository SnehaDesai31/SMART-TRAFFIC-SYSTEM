from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():

    data = request.get_json()

    road_type = data.get('road_type')
    vehicle = data.get('vehicle')

    # determine number of roads
    count = 1
    if road_type == "two":
        count = 2
    elif road_type == "three":
        count = 3
    elif road_type == "four":
        count = 4

    # collect densities
    roads = []
    for i in range(1, count+1):
        roads.append(int(data.get(f'r{i}', 0)))

    # emergency override
    if vehicle != "none":
        green = int(vehicle[-1])
        if green > count:
            green = 1
        emergency = True
    else:
        green = roads.index(max(roads)) + 1
        emergency = False

    # waiting time (inbuilt)
    wait = sum(roads) // count

    # congestion level
    max_density = max(roads)
    if max_density > 80:
        level = "Critical"
    elif max_density > 60:
        level = "High"
    elif max_density > 40:
        level = "Medium"
    else:
        level = "Low"

    return jsonify({
        "green": green,
        "wait": wait,
        "level": level,
        "emergency": emergency,
        "densities": roads,
        "count": count
    })

if __name__ == '__main__':
    app.run(debug=True)