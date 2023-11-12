from link import *
class Comment():
    """Comments belonging to a specific task.

    Attributes:
      commentId: the id of the comment
      commenterId: to note who left the comment
      taskId: the task to which the comment belongs to
      content: the content of the comment
      commentTime: when the comment was left
      lastUpdateTime: the last time the comment was updated
    """
    def __init__(self, taskid):
        self.task_id = taskid

    def get_all_comments(self):
        """Get all comments for a task_id"""
        # TODO make dates pretty format
        # TODO get commenter name using LEFT JOIN
        sql = 'SELECT c.*, u.userName \
               FROM TASK AS t \
               LEFT JOIN TASKCOMMENT AS c ON t.tId = c.taskId \
               LEFT JOIN TRASKUSER AS u ON c.commenterId = u.uId \
               WHERE t.tId = :taskid'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'taskid': self.taskid}))

    def add_comment(self, data: str):
        """Add a comment"""

    def delete_comment(self, comment_id):
        pass
