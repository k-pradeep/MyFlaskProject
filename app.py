from flask import Flask, render_template, url_for, request,redirect
import psycopg2
import datetime
import sys
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sql:///test.db'


class DB_connection():
    content = ''
    #date_created = datetime.date.today()
    date_created = datetime.datetime.now()
    #use database task_manager, user = postgres
    try:
        conn = psycopg2.connect("dbname=task_manager user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute(" CREATE TABLE IF NOT EXISTS task_list( id SERIAL PRIMARY KEY, content VARCHAR(200), date_created date); ")
        #cur = cur.close()
    except:
        print("Error while opening the connection")

    def insert(self):
        conn = psycopg2.connect("dbname=task_manager user=postgres password=postgres")
        cur = conn.cursor()
        sql_query = f"insert into task_list (content, date_created) VALUES('{self.content}', '{self.date_created}');"
        print(sql_query)
        result = self.cur.execute(sql_query)
        self.cur.execute('commit;')
        cur.close()
        print(result)

    def selectAll(self):
        #conn = psycopg2.connect("dbname=task_manager user=postgres password=postgres")
        cur = self.conn.cursor()
        # Retrieves all tasks from task_list table
        self.cur.execute("select * from task_list;")
        result_set = self.cur.fetchall()
        print(type(result_set))
        cur.close()
        return result_set

    def selectone(self,id):
        #conn = psycopg2.connect("dbname=task_manager user=postgres password=postgres")
        cur = self.conn.cursor()
        # Retrieves all tasks from task_list table
        self.cur.execute(f"select * from task_list where id = {id};")
        result_set = self.cur.fetchall()
        print(type(result_set))
        cur.close()
        return result_set

    def update(self, id):
        #id = 0
        date_created = datetime.datetime.now()
        query = f"update task_list set content='{self.content}', date_created = '{date_created}' where id = {id}; commit;"
        print(f'update query is {query}')
        result = self.cur.execute(query)
        return result

    def delete(self, id):
        try:
            conn = psycopg2.connect("dbname=task_manager user=postgres password=postgres")
            cur = conn.cursor()

            sql_query = f"delete FROM task_list WHERE id = {id}; commit;"
            print(sql_query)
            print(id)
            result = cur.execute(sql_query)
            #self.conn.commit()
            print(result)
            cur = conn.close()
            return result
        except:
            print(sys.exc_info()[0])
            return 0


    def __repr__(self):
        return '<Task created>'


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        #id of the attribute in the form
        task_content = request.form['content']
        new_task = DB_connection()
        new_task.content = task_content
        try:
            new_task.insert()
            return redirect("/")
        except:
            return 'Issue adding your task'
    else:

        all_tasks = DB_connection().selectAll()
        print(type(all_tasks))
        print(all_tasks)
        #all_tasks is list id, content,date_created
        return render_template('index.html', tasks=all_tasks)

@app.route('/update', methods=['POST','GET'])
def update():
    #id = request.args.get('id')
    #task_text = f"{request.args.get('task_text')}"
    if request.method == 'POST':
        print(request.form.items())
        mydict = {}
        for key, value in request.form.items():
            mydict[key] = value
            #print("key: {0}, value: {1}".format(key, value))
        print(f'my dict is {mydict}')
        # id of the attribute in the form
        new_task = DB_connection()
        new_task.content = mydict['task_text']
        #print(f'In POST method task_text is {task_text}')
        try:
            new_task.update(mydict['id'])
            return redirect("/")

        except:
            print(sys.exc_info()[0])
            return 'Issue updating your task'
    else:
        id = request.args.get('id')
        task_text = f"{request.args.get('task_text')}"

        print(f'id is {id}')
        task = DB_connection().selectone(id)
        print(task_text)
        #task_text= task[0][1]
        url = f"update.html?id={id}&task_text='{task_text}'"
        print(f"url is {url}'")
        return render_template("update.html",id=id,task_text=task_text)

@app.route("/delete/<int:id>")
def delete(id):
    try:
        print(id)
        task_to_delete = DB_connection().delete(id)
        print(f"delete to task is {task_to_delete}")
        return redirect("/")

    except:
        print(sys.exc_info()[0])
        return "Unable to delete the task"

if __name__ ==  "__main__":
    app.run(debug=True)
