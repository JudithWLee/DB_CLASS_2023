from link import *
from api.General import General
from api.sql import DB
class Comment(General):
    """Comments belonging to a specific task.

    Attributes:
      commentId: the id of the comment
      commenterId: to note who left the comment
      taskId: the task to which the comment belongs to
      content: the content of the comment
      commentTime: when the comment was left
      lastUpdateTime: the last time the comment was updated
    """
    def __init__(self, item_id = None):
        self.taskId = item_id
        self.table_name = "COMMENT"
        self.attributes = ["commentId","commenterId","taskId","content",
                           "commentTime","lastUpdateTime"]
        self.primary = "commentId"
        self.list_page = None
        self.detail_page = None
        self.generate_id = True

    # NOTE I think this should be done in task instead
    def get_all_comments(self):
        """Get all comments for a taskId"""
        # TODO make dates pretty format
        # TODO get commenter name using LEFT JOIN
        title = self.attributes.append("userName")
        sql = 'SELECT c.*, u.userName \
               FROM TASK t \
               LEFT JOIN TASKCOMMENT c ON t.tId = c.taskId \
               LEFT JOIN TRASKUSER u ON c.commenterId = u."userId" \
               WHERE t.tId = :taskid'
        data =  DB.fetchall(DB.execute_input(DB.prepare(sql),
                                             {'taskid': self.taskid}))
        return dict(zip(title, data))
