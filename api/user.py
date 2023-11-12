from link import *
from api.General import General
from api.sql import DB
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
        self.userId = userId.strip()
        self.table_name = "TrackUser"
        self.attributes = ['userId','userName','password','supervisorId',
                           'adderId']
        self.primary = "userId"

    def get_password(self):
        sql = 'SELECT u.PASSWORD FROM TRACKUSER u WHERE TRIM(u."userId") = :userId'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'userId': self.userId}))[0][0]

    def get_detail(self):
        sql = 'SELECT u.*, \
                      u_supervisor.userName supervisorName, \
                      u_adder.userName adderName \
               FROM TRACKUSER u \
               LEFT JOIN TRACKUSER u_supervisor \
               ON u.supervisorId = u_supervisor."userId" \
               LEFT JOIN TRACKUSER u_adder \
               ON u."adderId" = u_adder."userId" \
               WHERE u."userId" = :userId'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'userId': self.userId}))

    def create(self, userId, item_data):
        item_data['adderId'] = self.userId
        super().create(item_data)

    # cancel -> to previous page
