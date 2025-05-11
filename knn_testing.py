import pandas as pd
from sklearn.neighbors import NearestNeighbors

def convert_expenses(expenses):
    if expenses < 4000:
        return 1
    elif expenses < 7000:
        return 2
    elif expenses < 10000:
        return 3
    else:
        return 4

def evaluate_model(model, students, universities):
    correct = 0
    total = len(students)

    for _, row in students.iterrows():
        student_features = [[row['sat_verbal'], row['sat_math'], convert_expenses(row['expenses'])]]
        distances, indices = model.kneighbors(student_features)

        recommended_unis = universities.iloc[indices[0]]['name'].tolist()

        if any(row['university'].lower() == uni.lower() for uni in recommended_unis):
            correct += 1

    accuracy = correct / total
    return accuracy

if __name__ == "__main__":
    universities = pd.read_csv('universities.csv')
    X = universities[['sat-verbal', 'sat-math', 'expenses']]
    model = NearestNeighbors(n_neighbors=1)
    model.fit(X)

    students = pd.read_csv('students.csv')

    acc = evaluate_model(model, students, universities)
    print(f"Top-5 Recommendation Accuracy: {acc:.2%}")
