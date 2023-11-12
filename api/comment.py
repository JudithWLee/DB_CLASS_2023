from link import *
from api.General import General
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
    def __init__(self, item_id):
        self.taskId = item_id
        self.table_name = "COMMENT"
        self.attributes = ["commentId","commenterId","taskId","content",
                           "commentTime","lastUpdateTime"]
        self.primary = "commentId"

    # NOTE I think this should be done in task instead
    def get_all_comments(self):
        """Get all comments for a taskId"""
        # TODO make dates pretty format
        # TODO get commenter name using LEFT JOIN
        sql = 'SELECT c.*, u.userName \
               FROM TASK AS t \
               LEFT JOIN TASKCOMMENT AS c ON t.tId = c.taskId \
               LEFT JOIN TRASKUSER AS u ON c.commenterId = u."userId" \
               WHERE t.tId = :taskid'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'taskid': self.taskid}))
