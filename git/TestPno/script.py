from flask import Flask, render_template, request, jsonify
from getfromdb import getFromDB
app = Flask(__name__)

# Simuleer het verkrijgen van gegevens vanuit Python
def get_data(date):
    # Voer je Python-code uit om de gegevens op te halen
    data = getFromDB(date)
    #print(str(date))
    #data = [10.5, 20, 15, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
    #print(data)
    print("Button 1:" + str(button1))
    print("Button 2:" + str(button2))
    print("Button 3:" + str(button3))
    print("Button 4:" + str(button4))
    print("Button 5:" + str(button5))
    print("Prijs 1:" + str(len(str(prijs1))))
    return data

@app.route('/get-data', methods=['GET'])
def get_data_route():
    #selected_date = request.args.get('selectedDate')
    #print(str(selected_date))
    data = get_data(selected_date)
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        global selected_date
        selected_date = request.form['selectedDate']
        
        return render_template('index.html', selectedDate=selected_date)
    return render_template('indextest.html')

@app.route('/run-python', methods=['GET', 'POST'])
def run_python_code():
    if request.method == 'POST':
        global selected_date
        selected_date = request.form['selectedDate']
        # Voer hier je Python-code uit en retourneer het resultaat
        #print(str(selected_date))
        global button1
        global button2
        global button3
        global button4
        global button5
        global prijs1
        button1 = request.form.get('button1') == 'true'
        button2 = request.form.get('button2') == 'true'
        button3 = request.form.get('button3') == 'true'
        button4 = request.form.get('button4') == 'true'
        button5 = request.form.get('button5') == 'true'
        prijs1 = request.form.get('price1')
        keuken = 50
        
        result = "Dit is de uitvoer van de Python-code."
        return render_template('index.html', selectedDate=selected_date, result=result,keuken=keuken)
    return render_template('indextest.html')
@app.route('/page1.html')
def pagina1():
    return render_template('index.html')

@app.route('/page2.html')
def pagina2():
    weather_statuses = ['cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny', 'rainy', 'cloudy', 'sunny']
    return render_template('page2.html', weather_statuses=weather_statuses)

@app.route('/page3.html')
def pagina3():
    return render_template('page1.html')
if __name__ == '__main__':
    app.run()
#host='172.20.10.3'