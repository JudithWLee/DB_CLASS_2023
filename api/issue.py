from link import *
from api.filter import Filter
class Issue():
    """AKA task.

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
    def list_issue(user_filter: Filter):
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
               WHERE MID LIKE :id \
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
    def show_issue_detail(taskid):
        """Show issue detail based on taskid.

        Args:
            taskid (int): the id of the task

        Returns:
            task details
        """
        # TODO DUEDATE
        sql = 'SELECT t.*, \
                      u_owner.userName as ownerName, \
                      u_assigner.userName as assignerName, \
                      u_creator.userName as creatorName \
               FROM TASK AS t \
               LEFT JOIN TRACKUSER AS u_owner ON t.taskowner = u_owner.uId \
               LEFT JOIN TRACKUSER AS u_assigner ON t.assigner = u_assigner.uId \
               LEFT JOIN TRACKUSER AS u_creator ON t.creator = u_creator.uId \
               LEFT JOIN TASKCOMMENT AS c ON t.tId = c.tId \
               WHERE t.tId = :taskid'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'taskid': taskid}))

