from flask import Flask, request, render_template
import json, pymysql, time

app = Flask(__name__)
secret = "" # remove from git


class Database:
        def __init__(self):
            host = "localhost"
            user = "root"
            password = "mitiaxd"
            db = "Temp_Records"
            self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
            self.cur = self.con.cursor()
      
        def setNewTemp(self, temp, humidity):
            now = time.strftime('%Y-%m-%d %H-%M-%S')
            insertString = "INSERT INTO temps VALUES(NULL, '" + temp + "','" + humidity + "','" + now + "');"
            print(insertString)
            self.cur.execute(insertString)
            self.con.commit()

        def getAllTemps(self):
            self.cur.execute("SELECT id, temp, humidity, date FROM temps") #LIMIT 50")
            result = self.cur.fetchall()
            return result

        def getLastTemp(self):
            self.cur.execute("SELECT * FROM temps WHERE ID=(SELECT MAX(ID) FROM temps)")
            result = self.cur.fetchall()
            return result


@app.route('/set', methods=['POST'])
def set_temp():
        print("JSON?:", request.is_json)
        if not request.is_json:
            return "Should be JSON format"
        
        # Add exeptions for bad json
       # print(request.data)
        content = json.loads(request.data.decode('utf-8'), strict=False)
        print ("Temp: " + content['temp'])
        if content['secret'] != secret:
            return "Bad secret"
        
        db = Database()
        db.setNewTemp(content['temp'], content['humidity'])

        return "Success"


@app.route('/current')
def get_last_temp():
        db = Database()
        res = db.getLastTemp()
        return render_template('current_temp.html', result=res)



@app.route('/')
def temps_list():
        def db_query():
            db = Database()
            temps = db.getAllTemps()
            return temps
        res = db_query()
        return render_template('temp_table.html', result=res, content_type='application/json')





if __name__ == '__main__':
          app.run(host='0.0.0.0', port=1489, debug=True)
