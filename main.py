from flask import Flask,jsonify, request
import sqlite3

app = Flask(__name__)

#List all to dos.
@app.route("/all")
def viewAllList():
    allTask = []
    conn = sqlite3.connect('todo.db')
    cursor = conn.execute("SELECT Task, Status from todo ")
    
    for row in cursor:
        tasks = [{ 'Task': row[0], 'Status': row[1] }]
        allTask.append(tasks)
    conn.close()
    return jsonify(allTask)


# method to create a new to do list
def entryTask(inputText):
     
    defalut_Status = 'Not Done'
    new_task = [inputText,defalut_Status]
    message = 'Task Created: '+ inputText
    return new_task

# insert the data into database
def createNewDataEnry(data):
    conn = sqlite3.connect("todo.db")
    conn.execute("INSERT INTO todo (Task,Status) VALUES ('"+data[0]+"','"+data[1]+"')")
    conn.commit()
    conn.close()

@app.route('/add')
def add():
    task = request.args.get('task')
    data = entryTask(task)
    createNewDataEnry(data)
    return jsonify ([{ 'Task': data[0], 'Status': data[1] }])



#delete the data from the database
def deleteDataEntry(id):
    conn = sqlite3.connect('todo.db')
    conn.execute("DELETE from todo where ID = "+str(id)+";")
    conn.commit()
    conn.close()


@app.route('/delete')
def deleteTask():
    id = request.args.get('id')
    deleteDataEntry(int(id) ) 
    return("Task deleted!")



#update the entry in the database
def updateEntry(action,id):
    conn = sqlite3.connect('todo.db')
    conn.execute("UPDATE todo set Status = '"+action+"' where ID = "+str(id)+"")
    conn.commit()
    conn.close()

def markDone(id):
    updateEntry('done',id)

def markNotdone(id):
    updateEntry('Not Done', id)

#Mark a to do as "done" or "not done".
@app.route('/update')
def markTask():
    taskid = int(request.args.get('id'))
    userValue = request.args.get('value')
    if userValue =='done':
        markDone(taskid)
    elif userValue =='notdone':
        markNotdone(taskid)
    return ("Changes made successfully")

#Filter to dos on "done", "not done" and/or contains text.
def dbFilter(action):
    alltask = []
    conn = sqlite3.connect('todo.db')
    cursor = conn.execute("SELECT Task, Status from todo where Status = '"+ action+"'")
    for row in cursor:
        tasks = [{ 'Task': row[0], 'Status': row[1] }]
        alltask.append(tasks)
    conn.close()
    return alltask

@app.route('/filter')
def filter():
    action = request.args.get('value')
    if action == 'done':
        val = dbFilter('done')
        return jsonify(val)
    elif action =='notdone':
        val = dbFilter('Not Done')
        return jsonify(val)

if __name__ == '__main__':
    app.run(debug=True)