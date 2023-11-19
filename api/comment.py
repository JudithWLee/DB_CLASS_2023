from datetime import datetime
from link import *
from api.General import General
from api.sql import DB
from api.user import TrackUser
from api.global_vars import *
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
        self.table_name = "TASKCOMMENT"
        self.attributes = ["commentId","COMMENTERID",'taskId',"content",
                           "commentTime","lastUpdateTime"]
        self.primary = "commentId"
        self.list_page = None
        self.detail_page = None
        self.generate_id = True

    # NOTE I think this should be done in task instead
    def list_items(self):
        """Get all comments for a taskId"""
        # TODO make dates pretty format
        # TODO get commenter name using LEFT JOIN
        title = self.attributes.copy()
        title.append("commenterName")
        sql =  'SELECT c.commentId, c.commenterId, c.taskId, c.content, '
        sql += "TO_CHAR(c.commentTime, 'YYYY/MM/DD') commentTime, "
        sql +=f'c.lastUpdateTime, u.userName \
               FROM TASKCOMMENT c \
               LEFT JOIN TRACKUSER u ON c.commenterId = u."userId" \
               WHERE c.taskId = {self.taskId}'
        data = DB.fetchall(DB.execute(DB.connect(), sql))
        data_list = []
        for entry in data:
            data_list.append(dict(zip(title, entry)))
        return data_list

    def create(self, item_data: dict):
        # first set commenterid, taskid, comment time, and last updated time
        item_data['taskId'] = self.taskId
        item_data['commentTime'] = datetime.now()
        item_data['lastUpdateTime'] = datetime.now()
        item_data['COMMENTERID'] = GlobalVar().get_logged_in_user()
        super().create(item_data)
