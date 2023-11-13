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
    def __init__(self, userId = None):
        if userId is not None:
            self.userId = userId.strip()
        else:
            self.userId = userId
        self.table_name = "TrackUser"
        self.attributes = ['userId','userName','password','supervisorId',
                           'adderId']
        self.primary = "userId"
        self.list_page = "viewuser.html"
        self.detail_page = "userdetail.html"
        self.generate_id = False

    def get_password(self):
        sql = 'SELECT u.PASSWORD FROM TRACKUSER u WHERE TRIM(u."userId") = :userId'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'userId': self.userId}))[0][0]

    def list_items(self):
        title = self.attributes.copy()
        title.extend(['supervisorName', 'adderName'])
        sql = 'SELECT u.*, \
                      u_supervisor.userName supervisorName, \
                      u_adder.userName adderName \
               FROM TRACKUSER u \
               LEFT JOIN TRACKUSER u_supervisor \
               ON u.supervisorId = u_supervisor."userId" \
               LEFT JOIN TRACKUSER u_adder \
               ON u.adderId = u_adder."userId"'
        data = DB.fetchall(DB.execute(DB.connect(), sql))
        data_list = []
        for entry in data:
            data_list.append(dict(zip(title, entry)))
        return data_list

    def get_detail(self, userId):
        title = self.attributes.copy()
        title.extend(['supervisorName', 'adderName'])
        sql = 'SELECT u.*, \
                      u_supervisor.userName supervisorName, \
                      u_adder.userName adderName \
               FROM TRACKUSER u \
               LEFT JOIN TRACKUSER u_supervisor \
               ON u.supervisorId = u_supervisor."userId" \
               LEFT JOIN TRACKUSER u_adder \
               ON u.adderId = u_adder."userId" \
               WHERE u."userId" = :userId'
        data = DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'userId': userId}))
        print(data) # DEBUG
        return dict(zip(title, data[0]))

    def create(self, userId, item_data):
        item_data['adderId'] = self.userId
        super().create(item_data)

    # cancel -> to previous page
