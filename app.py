'''-------------------MAIN FLASK APPLICATION API------------------------'''
from shared import * #COMMON FLASK OBJECT FOR MODULAR PROGRAMMING
from get_recommendations import *
from generate_image import *
app.secret_key = "@@orbdoc@@patient@@symptomtracker"
CORS(app)
#HOME PAGE(PATIENT DETAILS)
@app.route('/', methods=["POST", "GET"])
def home0():
    return render_template('patient details.html')
#API TO RENDER SYMPTOM LOG PAGE
@app.route('/log_symptom', methods=["POST", "GET"])
def log_symptom():
    print(symptoms)
    return render_template('logsymptom.html',symptom=symptoms)
#API TO RENDER PAGE TO DISPLAY GRAPH
@app.route('/history', methods=["POST", "GET"])
def history():
    return render_template('history.html',symptom=symptoms,symptom_name=symptom_name)
#API TO RENDER RECOMMENDATIONS PAGE
@app.route('/recommendations', methods=["POST", "GET"])
def recommendations():
    return render_template('recommendations.html',description="",precaution=[],workout=[])
#API TO STORE PATIENT DETAILS TO DATABASE
@app.route("/details_to_db",methods=["POST","GET"])
def details_to_db():
    attribute_list=["p_id","p_name","age","contact"]
    value_list=[]
    for i in attribute_list:
            value_list.append(request.form[i])
    obj=pymysql.connect(host="localhost",user="root",password="2theeran7",database="patientsymptomtracker")
    cur=obj.cursor()
    try:
        cur.execute("Insert into patientdetails values"+str(tuple(value_list))+";")
        obj.commit()
        cur.close()
        obj.close()
        return "<H1 style='color:green;'>SUCCESSFULLY INSERTED PATIENT DETAILS</H1>"
    except:
        return "<h1 style='color:red;'>ERROR IN INSERTION OF PATIENT DETAILS</H1>"
#API TP STORE SYMPTOM LOG TO DATABSE
@app.route("/log_to_db",methods=["POST","GET"])
def log_to_db():
    attribute_list=["p_id","symptom","severity"]
    value_list=[]
    for i in attribute_list:
            value_list.append(request.form[i])
    obj=pymysql.connect(host="localhost",user="root",password="2theeran7",database="patientsymptomtracker")
    cur=obj.cursor()
    try:
        cur.execute("Insert into log(p_id,symptom,severity) values"+str(tuple(value_list))+";")
        obj.commit()
        cur.close()
        obj.close()
        return "<H1 style='color:green;'>SUCCESSFULLY INSERTED SYMPTOM LOG</H1>"
    except:
        return "<h1 style='color:red;'>ERROR IN INSERTION OF SYMPTOM LOG</H1>"
if __name__=="__main__":
    app.run(debug=True)



