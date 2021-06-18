from flask import Flask, request
from flask_restplus import Api, Resource, fields
import datetime
import sqlite3

# import sqlite
app = Flask(__name__)

api = Api(app, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API',
          )

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'due_date': fields.String(required=True, description='Due date for the task'),
    'status': fields.String(required=True, description='The task status')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, status):
        for todo in self.todos:
            if todo['id'] == id:
                todo['status'] = status
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)
        return "{Todo task deleted}"

    def get_overdue(self):
        overdue = []
        for todo in self.todos:
            str = todo['due_date']
            format = "%Y-%m-%d"
            task_date = datetime.datetime.strptime(str, format).date()
            today_date = datetime.date.today()
            if task_date < today_date and todo['status'].lower() != "Finished".lower():
                overdue.append(todo)
        if len(overdue) > 0:
            return overdue
        else:
            api.abort(404, "Todo {} doesn't exist".format(id))

    def get_finished(self):
        finished = []
        for todo in self.todos:
            if todo['status'].lower() == "Finished".lower():
                finished.append(todo)
        if len(finished) > 0:
            return finished
        else:
            api.abort(404, "Todo {} doesn't exist".format(id))

    def get_task_date(self, due_date):
        todos_dates = []
        for todo in self.todos:
            if todo['due_date'] == due_date:
                todos_dates.append(todo)
        if len(todos_dates) > 0:
            return todos_dates
        else:
            api.abort(404, "Todo {} doesn't exist".format(id))

DAO = TodoDAO()
conn = sqlite3.connect('todo.db')
print("Database connected successfully")
c=conn.cursor()
c.execute("select * from todolist")
for x in c:
    DAO.create({'task': x[1], 'due_date': x[2], 'status': x[3]})
#print(len(c))
#print(c.fetchone())


'''
DAO.create({'task': 'Submit the assignment', 'due_date': '2021-06-17', 'status': 'In progress'})
DAO.create({'task': 'Get the groceries', 'due_date': '2021-06-20', 'status': 'Finished'})
'''

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos



@ns.route('/create')
@ns.response(404, 'Todo not found')
@ns.param('password', 'Enter password')
@ns.param('username', 'Enter username')
@ns.doc('create_todo')
class TodoList(Resource):
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        if request.args.get('username')=='sneha' and request.args.get('password')=='ssn':
         return DAO.create(api.payload), 201
        else:
            api.abort(401, "You are not authorised to create a task".format(id))

@ns.route('/due')
@ns.response(404, 'Todo not found')
@ns.param('due_date', 'Enter due date(yyyy-mm-dd)')
class Todo(Resource):
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        due_date = request.args.get('due_date')
        return DAO.get_task_date(due_date)


@ns.route('/overdue')
@ns.response(404, 'Todo not found')
class Todo(Resource):
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        return DAO.get_overdue()


@ns.route('/finished')
@ns.response(404, 'Todo not found')
class Todo(Resource):
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        return DAO.get_finished()


@ns.route('/<int:id>/<string:status>')
@ns.response(404, 'Todo not found')
@ns.param('status', 'The task status')
@ns.param('id', 'The task identifier')
@ns.param('password','Enter password')
@ns.param('username','Enter  username')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id, status):
        '''Update the status of a task given its identifier'''
        if request.args.get('username')=='sneha' and request.args.get('password')=='ssn':
         return DAO.update(id, status)
        else:
            api.abort(401, "You are not authorised to update status of the task".format(id))
@ns.route('/<int:id>/')
@ns.param('id', 'The task identifier')
@ns.param('password','Enter password')
@ns.param('username','Enter  username')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        if request.args.get('username')=='sneha' and request.args.get('password')=='ssn':
         DAO.delete(id)
         return '', 204
        else:
            api.abort(401, "You are not authorised to delete a task".format(id))




if __name__ == '__main__':
    str = "2021-06-10"
    format = "%Y-%m-%d"
    print(datetime.datetime.strptime(str, format).date())
    today = datetime.date.today()
    print(today)
    app.run(debug=True)
