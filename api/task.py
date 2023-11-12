from link import *
from api.filter import Filter
from api.General import General
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
    def __init__(self, item_id):
        self.taskId = taskId
        self.table_name = "Task"
        self.attributes = ["taskId","status","description","taskOwner","title",
                           "dueDate","assigner","creator","assigntime"]
        self.primary = "taskId"

    def list_item(user_filter: Filter):
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
        sql = "SELECT * FROM TASK \
               WHERE TASKOWNER LIKE :id \
               AND STATUS LIKE :status \
               AND TITLE LIKE '%:keyword%' \
               ORDER BY :order_by :order"
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'id': user_filter.user,
                                             'status': user_filter.status,
                                             'keyword': user_filter.keyword,
                                             'order_by': user_filter.order_by,
                                             'order': user_filter.order}))

    # TASKCOMMENT
    # TASK
    # TRACKUSER
    def get_detail(taskid):
        """Show task detail based on taskid.

        Args:
            taskid (int): the id of the task

        Returns:
            task details
        """
        sql = 'SELECT t.taskId, t.status, t.description, t.taskOwner, t.title, \
                      TO_CHAR(t.dueDate, "YYYY/MM/DD") AS dueDate, \
                      t.assigner, t.creator, t.assigntime, \
                      u_owner.userName as ownerName, \
                      u_assigner.userName as assignerName, \
                      u_creator.userName as creatorName \
               FROM TASK AS t \
               LEFT JOIN TRACKUSER AS u_owner ON t.taskowner = u_owner."userId" \
               LEFT JOIN TRACKUSER AS u_assigner ON t.assigner = u_assigner."userId" \
               LEFT JOIN TRACKUSER AS u_creator ON t.creator = u_creator."userId" \
               LEFT JOIN TASKCOMMENT AS c ON t.taskId = c.taskId \
               WHERE t.taskId = :taskid'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'taskid': taskid}))

