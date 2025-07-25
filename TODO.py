from flask import Flask, render_template,request,redirect,url_for,jsonify
from modules.cloud import TODO,cloudError

server = Flask(__name__)

def prepare_dataset_todo():    
    todo_obj = TODO()
    dataset = {}

    cloud_data = todo_obj.viewDatas()

    # check whether the database is empty or not
    if cloud_data == []:
        return {0:["","Create Your First TODO", "Want to do It" , "in-complete" , "00:00:00"]}
    
    for data in cloud_data:

        key = data[0]  # ID
        tag = data[3]
        value = list(data[1:])  # [task, status, datetime]

        # Determine if class name should be added
        if tag.upper() == "COMPLETED":
            value.insert(0, "accomplished")
        elif tag.upper() == "PROGRESS":
            value.insert(0, "progress")
        elif tag.upper() == "IN-COMPLETE":
            value.insert(0, "")
        elif tag.upper() == "CANCELLED":
            value.insert(0, "cancelled")
        else:
            raise cloudError("whether is the tag --->"+tag)

        dataset[key] = value
    return dataset


@server.route("/")
@server.route("/todo")
def todo_main_page():
    dataset = prepare_dataset_todo()
    print(dataset)
    sorted_dataset = dict(sorted(dataset.items() , key= lambda item : item[1][4] , reverse=True))
    return render_template("index.html",backend=sorted_dataset)


@server.route("/addTodo",methods=["POST"])
def adding_todo_data():
    
    task = request.form.get("task")
    status = request.form.get("status")
    tag = request.form.get("tag")
    print(task,status,tag)
    print(request.form)
    # input("---------")
    todo = TODO()
    todo.addData(task, status, tag) # type: ignore

    return redirect(url_for("todo_main_page"))

@server.route("/deleteTodo",methods=["POST"])
def delete_todo_data():
    data = request.get_json()
    id = data.get("id")
    
    if not data:
        return "no data"
    todo = TODO()
    todo.deleteData(id=id)

    return redirect(url_for("todo_main_page"))

@server.route("/editTodo", methods=["POST"])
def update_todo_data():
    
    form = request.get_json()
    print("form --> ",form)
    id = form.get("id")
    task = form.get("task")
    status = form.get("status")
    tag = form.get("tag")

    todo = TODO()
    todo.updateData(id,task=task,status=status,tag=tag)

    return jsonify({"redirect":url_for("todo_main_page")})


if __name__ == "__main__":
    server.run(port=2006, debug=True)
