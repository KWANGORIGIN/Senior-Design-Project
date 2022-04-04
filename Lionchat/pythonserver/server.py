from typing import List, Dict
from flask import Flask
import json
from mysql.connector import connect
from datetime import datetime
from datetime import tzinfo, timedelta, datetime

app = Flask(__name__)

@app.route('/answer_events', methods=["POST"])
def get_events():
    #default message
    message = "Here's what I found for this week:"
    
    #get request from Spring Boot application containing query
    if isinstance(request.json, str):
        text = jsonify(request.json)["utterance"]
    else:
        text = request.json["utterance"]
        text = str.replace(text, "\'", "\\'")
        
    entities = []
    
    try:
        entities = ner.getEnts(text) # get entities from user query
    except:
        print("NER model not found")
        
    
    #if entities are present
    if entities:
        #initialize some booleans
        more_entities = False
        set_date = False
        set_name = False
        sql = "SELECT EVTNAME, ORG, LOC, DATE, URL FROM events WHERE " # begin sql query on events table
        
        #find current day for use in query
        current_day = datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        date1 = current_day
        date2 = date1
        
        #by default, get events happening this week, so time span is set for current day till end of week
        while date2.weekday() != 6:
            date2 += timedelta(days=1)
        date2 += timedelta(days=1)

        
        for ent in entities:
            label = ent.label_
            text = ent.text.replace("?", "") #replace question mark if was accidentally returned
            
            if label == 'EVTNAME': #if event name was input, get all future dates instead of one week
                set_name = True
            
            if more_entities and label != 'DATE': #if date was entered, set time span accordingly
                sql = sql + " AND " 
            
            if label == 'DATE':
                set_date = True

                if text == 'today':
                    date2 = date1 + timedelta(days=1)
                    message = "Here's what I found for today:"

                elif text == 'tomorrow':
                    date1 = current_day + timedelta(days=1)
                    date2 = date1 + timedelta(days=1)
                    message = "Here's what I found for tomorrow:"
                
                elif text == 'next week':
                    date1 += timedelta(weeks = 1)
                    date2 = date1
                    
                    while date1.weekday() != 0:
                        date1 -= timedelta(days = 1)
                    while date2.weekday() != 6:
                        date2 += timedelta(days = 1)
                    date2 += timedelta(days=1)   
                    message = "Here's what I found for next week:"
                    
                elif text == 'this month':
                    date2 = date1
                    month = date1.month
                    while date2.month == month:
                        date2 += timedelta(days = 1)
                    message = "Here's what I found for this month:"
                elif text != 'this week':
                    message = "I'm sorry, that time-frame was not recognized.  Here are today's events:"
                    date2 = date1 + timedelta(days=1)

            else:
                
                print(text)
                sql = sql +  "LOWER({}) like '%{}%'".format(label, text)
                more_entities = True
            
        
        for ent in entities:
            print(ent.label_, ent.text)
         
         
        if more_entities:
            sql = sql + " AND " #add more entities to search in the database
            
        #if event name was set
        if set_name:
            message = "Here's what I found for this event:"
     
        if not set_date and set_name: #if name entered and date not entered, query all future dates for event
            sql += "DATE >= {}".format(int(date1.timestamp()))
        else: #otherwise query between whatever dates were set
            sql += "DATE BETWEEN {} AND {}".format(int(date1.timestamp()), int(date2.timestamp()) - 1)
        #print(sql)
        #print(date1)
        #print(datetime.fromtimestamp(date2.timestamp() - 1))
        
        #make sure program does not crash if database missing
        try:
            config = {
                'user': 'root',
                'password': 'root',
                'host': 'db',
                'port': '3306',
                'database': 'ml_database'
            }
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            cursor.execute(sql)
        
            evt_list = list(cursor)
            cursor.close()
            connection.close()
 
            for i in range(len(evt_list)):
                evt_list[i] = list(evt_list[i])
                evt_list[i][0] = "Event Name: " + evt_list[i][0]
                evt_list[i][1] = "Event Organizer: " + evt_list[i][1]
                evt_list[i][2] = "Event Location: " + evt_list[i][2]
                evt_list[i][3] = "Event Date: " + str(datetime.fromtimestamp(int(evt_list[i][3])).strftime("%m/%d/%Y, %H:%M:%S"))
                evt_list[i][4] = "Event Link: " + evt_list[i][4]
        except Exception as e:
            print(e)
            print("Can't access database")
            evt_list = ["Database error."]
            
        if evt_list: #if events found
            payload = jsonify(message = message, events = evt_list)
        else: #if nothing found
            payload = jsonify(message = "It looks like I don't have any information on that.", events = [evt_list])
        
        
    else: #if no entities were present
        payload = jsonify(message = 'I am sorry, I need more data.  Can you be more specific?', events = [])
        
     #EVTNAME
     #LOC
     #DATE
     #ORG

    return payload

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)