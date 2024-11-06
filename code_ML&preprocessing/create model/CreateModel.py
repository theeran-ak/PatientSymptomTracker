'''---------------TO CREATE THE DECISION TREE MODEL TO PROVIDE RECOMMENDATIONS--------------'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn import tree
import joblib
import matplotlib.pyplot as plt

data = pd.read_csv("training.csv")

X = data.drop(columns=['prognosis'])   # features
y = data['prognosis']                  # Target 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(random_state=42) # Decision Tree
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test) #predict

#EVALUATION
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save the trained model to a file
clf.fit(X, y)
joblib.dump(clf, 'disease_prediction_model.joblib')
