'''-----------------------API TO PROVIDE THE RECOMMENDATIONS FOR PATIENT SYMPTOMS------------------------'''

'''THE MAIN LOGIC BEHIND RECOMMENDATION GENERATION
--- A Decision Tree Model is used to predict the disease that the patient might have based on the recent symptoms
logged by the patient.
--- The recommendations are searched in the 'symptom.json' to provide the appropriate recommendations
'''
from shared import *
@app.route('/get_recommendations', methods=["POST", "GET"])
def get_recommendations():
    obj=pymysql.connect(host="localhost",user="root",password="2theeran7",database="patientsymptomtracker")
    cur=obj.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#current date
    query = """
        SELECT * FROM log 
        WHERE p_id = %s AND logdate >= DATE_SUB(%s, INTERVAL 7 DAY)
    """
    p_id = request.form["p_id"] 
    cur.execute(query, (p_id, current_date))
    recent_logs = cur.fetchall()
    for log in recent_logs:
        print(log)
    cur.close()
    obj.close()
    log_dict = {}
    for log in recent_logs:
        log_datetime = log[1]
        symptom = log[2]
        severity = log[3]

        datetime_tuple = (log_datetime.year, log_datetime.month, log_datetime.day,
                        log_datetime.hour, log_datetime.minute, log_datetime.second)
        
        log_dict[datetime_tuple] = [symptom, severity]
    print(log_dict)
    test_symptom=[]
    for i in log_dict:
        test_symptom.append(log_dict[i][0])

    # load model(decision tree classifier)
    clf = joblib.load('static/model/disease_prediction_model.joblib')
    with open("static/symptom.json", "r") as json_file:
        symptom_type = json.load(json_file)
    sym = symptom_type["Symptom"]
    print(len(sym))
    X_test=[]
    for i in sym:
        if(i in test_symptom):
            X_test.append(1)
        else:
            X_test.append(0)
    y_pred = clf.predict([X_test])# Make predictions
    print(y_pred)
    with open("static/disease_data.json", "r") as json_file:
        disease_data = json.load(json_file)
    disease_name = y_pred[0]
    disease_info = disease_data[disease_name]  # Direct access using the key
    description=disease_info["Description"]
    precaution=disease_info["Precaution"]
    workout=disease_info["Workout"]
    return render_template('recommendations.html',description=description,precaution=precaution,workout=workout)
