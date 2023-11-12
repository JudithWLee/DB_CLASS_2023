from link import *
from api.General import General
class TrackUser(General):
    """Tracker users

    Attributes:
      userId: the Id of the user
      userName: the name of the user
      password: the password of the user
      supervisorId: the Id of the supervisor of the user
      adderId: the Id of the person adding the user to the tracker
    """
    def __init__(self, userId):
        self.userId = "userId"
        self.table_name = "TrackUser"
        self.attributes = ['userId','userName','password','supervisorId',
                           'adderId']
        self.primary = "key"

    def get_detail(self):
        sql = 'SELECT u.*, \
                      u_supervisor.userName as supervisorName, \
                      u_adder.userName as adderName \
               FROM TRACKUSER AS u \
               LEFT JOIN TRACKUSER AS u_supervisor \
               ON u.supervisorId = u_supervisor."userId" \
               LEFT JOIN TRACKUSER AS u_adder \
               ON u.adderId" = u_adder."userId" \
               WHERE u."userId" = :userId'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'userId': self.userid}))

    def create(self, userId, item_data):
        item_data['adderId'] = self.userId
        super().create(item_data)

    # cancel -> to previous page
