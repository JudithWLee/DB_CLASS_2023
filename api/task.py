from link import *
from api.filter import Filter
from api.General import General
from api.sql import DB
from datetime import datetime
from api.global_vars import GlobalVar
class Task(General):
    """AKA issue.

    Attributes:
      taskId: the id of the task
      status: the status of the task
        open, inprogress, review, or close
      description: the description of the task
      taskOwner: the id of the owner of the task
      title: the title of the task
      dueDate: when the task will due
      assigner: the person assigning the task
      creator: the person created the task
      assigntime: when the task was assigned
    """
    def __init__(self, item_id = None):
        self.taskId = item_id
        self.table_name = "Task"
        self.attributes = ["taskId","status","description","taskOwner","title",
                           "dueDate","assigner","creator","AssignTime"]
        self.date_attributes = ["dueDate", "AssignTime"]
        self.primary_sql = '"taskId"'
        self.primary_python = 'taskId'
        self.list_page = "viewissue.html"
        self.detail_page = "issuedetail.html"
        self.generate_id = True

    def debugger(self, msg):
        print(msg)

    def list_item(self, user_filter: Filter):
        """Lists all tasks.

        By default, list all tasks available in order of task id;
        if user specifies filter, show by filter.
        Possible filters:
        - task owner
        - status

        Possible sorts:
        - due date

        Can also search by keyword

        Args:
            user_filter (Filter): specified filter

        Returns:
            filtered tasks
        """
        title = self.attributes.copy()
        title.append('ownerName')
        data_list = []
        sql = 'SELECT t."taskId", t.status, t.description, t.taskOwner, t.title, '
        sql += "      TO_CHAR(t.dueDate, 'YYYY/MM/DD') dueDate, \
                      t.assigner, t.creator, TO_CHAR(t.assigntime, 'YYYY/MM/DD') assignTime, \
                      u_owner.userName ownerName "
        sql += 'FROM TASK t '
        sql += 'LEFT JOIN TRACKUSER u_owner ON t.taskowner = u_owner."userId" '
        sql += f"WHERE u_owner.userName LIKE '{user_filter.user}' \
                AND t.STATUS LIKE '{user_filter.status}' \
                AND t.TITLE LIKE '%{user_filter.keyword}%' \
                ORDER BY {user_filter.order_by} {user_filter.order}"
        data = DB.fetchall(DB.execute(DB.connect(), sql))
        for entry in data:
            data_list.append(dict(zip(title, entry)))
        return data_list

    # TASKCOMMENT
    # TASK
    # TRACKUSER
    def get_detail(self, taskid):
        """Show task detail based on taskid.

        Args:
            taskid (int): the id of the task

        Returns:
            task details
        """
        print(f"get detail taskid: {taskid}") # DEBUG
        title = self.attributes.copy()
        title.extend(['ownerName', 'assignerName','creatorName'])

        sql = 'SELECT t."taskId", t.status, t.description, t.taskOwner, t.title, '
        sql += "      TO_CHAR(t.dueDate, 'YYYY/MM/DD') dueDate, \
                      t.assigner, t.creator, TO_CHAR(t.assigntime, 'YYYY/MM/DD') assignTime, \
                      u_owner.userName ownerName, \
                      u_assigner.userName assignerName, \
                      u_creator.userName creatorName \
               FROM TASK t "
        sql += 'LEFT JOIN TRACKUSER u_owner ON t.taskowner = u_owner."userId" \
               LEFT JOIN TRACKUSER u_assigner ON t.assigner = u_assigner."userId" \
               LEFT JOIN TRACKUSER u_creator ON t.creator = u_creator."userId" \
               WHERE t."taskId" = :taskid'
               # deleted: LEFT JOIN TASKCOMMENT c ON t."taskId" = c."taskId" \

        data = DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'taskid': taskid}))
        return dict(zip(title, data[0]))

    def edit(self, item_data: dict):
        # preprocess task owner and assigner names
        sql = f'SELECT u."userId" \
               FROM TRACKUSER u '
        sql+= f"WHERE u.userName = '{item_data['taskOwner']}'"
        taskOwner = DB.fetchall(DB.execute(DB.connect(),sql))[0][0]
        sql = f'SELECT u."userId" \
               FROM TRACKUSER u '
        sql+= f"WHERE u.userName = '{item_data['Assigner']}'"
        Assigner = DB.fetchall(DB.execute(DB.connect(),sql))[0][0]

        item_data['taskOwner'] = taskOwner
        item_data['Assigner'] = Assigner
        return super().edit(item_data)

    def create(self, item_data: dict):
        # preprocess task owner and assigner names
        item_data['creator'] = GlobalVar().get_logged_in_user()
        if item_data['taskOwner'] not in (None, ''):
            sql = f'SELECT u."userId" \
                   FROM TRACKUSER u '
            sql+= f"WHERE u.userName = '{item_data['taskOwner']}'"
            taskOwner = DB.fetchall(DB.execute(DB.connect(),sql))[0][0]
            item_data['taskOwner'] = taskOwner

        if item_data['Assigner'] not in (None, ''):
            sql = f'SELECT u."userId" \
                   FROM TRACKUSER u '
            sql+= f"WHERE u.userName = '{item_data['Assigner']}'"
            Assigner = DB.fetchall(DB.execute(DB.connect(),sql))[0][0]
            item_data['Assigner'] = Assigner

        return super().create(item_data)
