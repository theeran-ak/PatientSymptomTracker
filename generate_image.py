'''----------------------API TO GENERATE THE GRAPH FOR SYMPTOM HISTORY-------------------------'''
from shared import * #connects all the modules
@app.route('/generate_image', methods=["POST", "GET"])
def generate_image():
    pid=request.form["p_id"]
    symptom_name=request.form["symptom"]
    obj=pymysql.connect(host="localhost",user="root",password="2theeran7",database="patientsymptomtracker")
    cur=obj.cursor()
    if symptom_name=="common":
            query = """
            SELECT * FROM log 
            WHERE p_id = %s
            """
            cur.execute(query, pid)
            history_logs = cur.fetchall()
    else:
            query = """
            SELECT * FROM log 
            WHERE p_id = %s and symptom= %s
            """
            cur.execute(query, (pid,symptom_name))
            history_logs = cur.fetchall()
    log_dict = {}
    for log in history_logs:
        log_datetime = log[1]
        symptom = log[2]
        severity = log[3]
        # datetime to a tuple conversion
        datetime_tuple = (log_datetime.year, log_datetime.month, log_datetime.day,
                        log_datetime.hour, log_datetime.minute, log_datetime.second)
        
        log_dict[datetime_tuple] = [symptom, severity]

    print(log_dict)
    # dictionary to a list (datetime, symptom, severity)
    data = [
        (datetime(*key), symptom[0], symptom[1])
        for key, symptom in log_dict.items()
    ]
    # Organize data by symptom
    symptom_data = defaultdict(list)
    for dt, symptom, severity in data:
        symptom_data[symptom].append((dt, severity))
    #PLOTTING
    if symptom_name=="common":
        plt.figure(figsize=(12, 6))
        for symptom, entries in symptom_data.items():
            entries.sort() # sort by datetime
            print(entries)
            dates, severities = zip(*entries)
            plt.plot(dates, severities, marker='o', label=symptom)
        plt.xlabel('Date and Time')
        plt.ylabel('Severity')
        plt.title('pid:'+pid+' Symptom History Over Time')
        plt.legend(title="Symptoms", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45) 
        plt.tight_layout()
    else:
        for symptom, entries in symptom_data.items():
            entries.sort()
            print(entries)
            dates, severities = zip(*entries)
        plt.figure(figsize=(10, 5))
        print(dates,severities)
        plt.bar(dates, severities, color='skyblue',width=0.2)
        plt.xlabel('Date and Time(hour)')
        plt.ylabel('Severity')
        plt.title(f'pid: {pid} Severity Trend for Symptom: {symptom_name}')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    # save the graph(IMAGE)
    img_path = f'static/images/{symptom_name}.png'
    plt.savefig(img_path)
    plt.close()  
    return render_template('history.html',symptom=symptoms,symptom_name=symptom_name,img_path="static/images/"+symptom_name+".png")
