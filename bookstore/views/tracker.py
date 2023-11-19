import inspect
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.feature import Feature
from api.task import Task
from api.comment import Comment
from api.filter import Filter
from api.user import TrackUser

tracker = Blueprint('tracker', __name__, template_folder='../templates')

class Tracker():
    def __init__(self, request_args: dict):
        table_class = {
            "task": Task,
            "issue": Task,
            "user": TrackUser,
            "feature": Feature,
            "comment": Comment
        }
        self.target_table = request_args["target_table"].lower()
        # general item id
        self.item_id = request_args.get("id", None)
        self.my_table = table_class[self.target_table](self.item_id)
        self.target_filter = request_args.get("filter", None)
        # for deleting comments, as we need still need to render the task
        self.task_id = request_args.get("task_id", None)
        # for adding comments
        # TODO do other creating item functions use this as well?
        self.content = (dict(request.form))

    def show_detail(self):
        target_data = self.my_table.get_detail(self.item_id)
        if self.target_table in ("task", "issue"):
            comments = Comment(self.item_id)
            comment_list = comments.list_items()
            return render_template(self.my_table.detail_page,
                                   item_detail = target_data,
                                   comment_list = comment_list)
        else:
            return render_template(self.my_table.detail_page,
                                   item_detail = target_data)

    def list_table(self):
        if self.target_table in ('task', 'issue'):
            return self._list_task()

        target_data = self.my_table.list_items()
        if target_data is None:
            target_data = []
        print(target_data) # DEBUG
        return render_template(self.my_table.list_page, item_list = target_data)

    def _list_task(self):
        # TODO finish filter implementation
        self.filter = Filter()
        self.my_table = Task()
        data = self.my_table.list_item(self.filter)
        return render_template(self.my_table.list_page, item_list = data)

    def delete(self):
        self.my_table.delete(self.item_id)
        if self.target_table == "comment":
            # setting things back to task so that we can show the task detail
            self.my_table = Task()
            self.item_id = self.task_id
            return self.show_detail()
        else:
            return self.list_table()

    def new(self):
        print(self.content) # DEBUG
        if self.target_table == "comment":
            self.my_table = Comment(self.task_id)
            self.my_table.save(self.content)
            # setting things back to task so that we can show the task detail
            self.my_table = Task()
            self.item_id = self.task_id
        else:
            new_id = self.my_table.save(self.content)
            self.item_id = new_id
        return self.show_detail()

    # TODO finish
    def empty_form(self):
        empty_data = self.my_table.empty_form()
        return render_template(self.my_table.detail_page, form = empty_data)

# routing functions
@tracker.route('/show_detail')
def show_detail():
    my_tracker = Tracker(request.args)
    return my_tracker.show_detail()

@tracker.route('/list_table')
def list_table():
    my_tracker = Tracker(request.args)
    return my_tracker.list_table()

@tracker.route('/delete', methods=['GET', 'POST'])
def delete():
    my_tracker = Tracker(request.args)
    return my_tracker.delete()

@tracker.route('/empty_form')
def empty_form():
    my_tracker = Tracker(request.args)
    return my_tracker.empty_form()

@tracker.route('/new', methods=['GET', 'POST'])
def new():
    print("new!") # DEBUG
    my_tracker = Tracker(request.args)
    return my_tracker.new()

@tracker.route('/save', methods=['GET', 'POST'])
def save():
    pass
