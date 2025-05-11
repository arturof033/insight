from flask import Flask, request, render_template
import pandas as pd
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

universities = pd.read_csv('universities.csv')
X = universities[['sat-verbal', 'sat-math', 'expenses']]
model = NearestNeighbors(n_neighbors=5)
model.fit(X)

@app.route('/', methods=['GET', 'POST'])
def index():

    recommendations = []

    if request.method == 'POST':
        sat_verbal = int(request.form['sat-verbal'])
        sat_math = int(request.form['sat-math'])
        expenses = int(request.form['expenses'])
        
        expenses = convert_expenses(expenses)


        user_input = [[sat_verbal, sat_math, expenses]]
        distances, indices = model.kneighbors(user_input)

        recommendations = universities.iloc[indices[0]].to_dict(orient='records')

        expense_map = {
            1: 'Less than $4,000',
            2: '$4,000 - $7,000',
            3: '$7,000 - $10,000',
            4: 'More than $10,000'
        }
        control_map = {
            1: 'private',
            2: 'public',
            3: 'state',
            4: 'city'
        }

        for rec in recommendations:
            rec['expenses'] = expense_map.get(rec['expenses'], 'Unknown')
            rec['control'] = control_map.get(rec['control'], 'Unknown')

    return render_template('form.html', recommendations=recommendations)

def convert_expenses(expenses):
    if(expenses < 4000):
        expenses = 1
    elif (expenses >= 4000 and expenses < 7000):
        expenses = 2
    elif (expenses >= 7000 and expenses < 10000):
        expenses = 3
    else:
        expenses = 4
    return expenses

if __name__ == '__main__':
    app.run(debug=True)
