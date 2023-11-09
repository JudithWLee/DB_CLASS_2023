from typing import Optional
from link import *

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Filter():
    def __init__(self):
        self.user = %
        self.status = %
        self.keyword = ''
        self.order_by = 'due date'
        self.order = 'DESC'
        self.featureId = None

    def get_all_member():
        # TODO remember to add "all"
        sql = "SELECT userName FROM GROUP5.TRACKUSER ;"
        return DB.fetchall(DB.execute_input(DB.prepare(sql)))

    def get_all_feature():
        sql = "SELECT userName FROM GROUP5.FEATURE ;"
        return DB.fetchall(DB.execute_input(DB.prepare(sql)))

    def set_member_filter(self):
        pass
    
    def set_status_filter(self):
        pass

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_feature(self, feature):
        self.featureId = featureId

    def set_order(self, order_by, order) -> None:
        self.order_by = order_by
        self.order = order

class Feature():
    def __init__(self, featureId = None, keyword: str = None):
        self.featureId = featureId
        self.keyword = keyword

    def list_features():
        sql = "SELECT f.*,
                      u_creator.userName as creatorName,
                      u_maintainer.userName as maintainerName,
               FROM FEATURE AS f
               LEFT JOIN TRACKUSER AS u_creator ON f.creatorId = u_creator.uId
               LEFT JOIN TRACKUSER AS u_maintainer ON t.maintainerId = u_maintainer.uId
               WHERE f.title LIKE '%:keyword%'
               OR f.descript LIKE '%:keyword%'"
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'keyword': self.keyword}))


    def get_details():
        sql = 'SELECT f.*,
                      u_creator.userName as creatorName,
                      u_maintainer.userName as maintainerName,
               FROM FEATURE AS f
               LEFT JOIN TRACKUSER AS u_creator ON f.creatorId = u_creator.uId
               LEFT JOIN TRACKUSER AS u_maintainer ON t.maintainerId = u_maintainer.uId
               WHERE f.featuerId = :featureId'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'featureId': self.featureId}))

    def list_tasks():
        """Get details of feature.

        Returns:
        - all details of tasks belonging to this feature
        """
        # TODO modify to show names, no filter
        sql = "SELECT t.*,
               FROM FEATURE AS f,
               LEFT JOIN FEATURETASKRELATION AS r ON f.featureId = r.featureId
               LEFT JOIN TASK AS t ON r.taskId = t.taskId
               WHERE f.featureId = :featureId"
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'featureid': self.featureId}))

class Issue():
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
        sql = "SELECT * FROM TASK
               WHERE MID LIKE :id
               AND STATUS LIKE :status
               AND TITLE LIKE '%:keyword%'
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
        sql = 'SELECT t.*,
                      u_owner.userName as ownerName,
                      u_assigner.userName as assignerName,
                      u_creator.userName as creatorName
               FROM TASK AS t
               LEFT JOIN TRACKUSER AS u_owner ON t.taskowner = u_owner.uId
               LEFT JOIN TRACKUSER AS u_assigner ON t.assigner = u_assigner.uId
               LEFT JOIN TRACKUSER AS u_creator ON t.creator = u_creator.uId
               LEFT JOIN TASKCOMMENT AS c ON t.tId = c.tId
               WHERE t.tId = :taskid'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'taskid': taskid}))
class Comment():
    def __init__(self, taskid):
        self.task_id = taskid

    def get_all_comments(self):
        """Get all comments for a task_id"""
        # TODO make dates pretty format
        # TODO get commenter name using LEFT JOIN
        sql = 'SELECT c.*, u.userName 
               FROM TASK AS t
               LEFT JOIN TASKCOMMENT AS c ON t.tId = c.taskId
               LEFT JOIN TRASKUSER AS u ON c.commenterId = u.uId
               WHERE t.tId = :taskid'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'taskid': self.taskid}))

    def add_comment(self, data: str):
        """Add a comment"""

    def delete_comment(self, comment_id):
        pass

class Member():
    def get_member(account):
        sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id' : account}))
    
    def get_all_account():
        sql = "SELECT ACCOUNT FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        sql = 'INSERT INTO MEMBER VALUES (null, :name, :account, :password, :identity)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(tno, pid):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and PID=:pid '
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pid':pid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       
class Product():
    def count():
        sql = 'SELECT COUNT(*) FROM PRODUCT'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_product(pid):
        sql ='SELECT * FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))

    def get_all_product():
        sql = 'SELECT * FROM PRODUCT'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO PRODUCT VALUES (:pid, :name, :price, :category, :description)'

        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(pid):
        sql = 'DELETE FROM PRODUCT WHERE PID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME=:name, PRICE=:price, CATEGORY=:category, PDESC=:description WHERE PID=:pid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'tno':tno}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    

class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order():
        sql = 'SELECT OID, NAME, PRICE, ORDERTIME FROM ORDER_LIST NATURAL JOIN MEMBER ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def category_sale():
        sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))
