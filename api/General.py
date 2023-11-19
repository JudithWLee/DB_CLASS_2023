from link import *
from api.sql import DB
class General():
    """Parent class for TrackUser, Task, Comment, and Feature.

    DO NOT call this directly."""
    def __init__(self, item_id: None):
        self.item_id = item_id
        self.table_name = "GENERAL"
        self.attributes = []
        self.primary = "key"
        self.generate_id = False

    def list_items(self):
        """List items per filter.

        This function needs to be overridden by child classes as the way things
        are filtered differ from table to table.
        """

    def get_detail(self):
        """Get item details.

        This function needs to be overridden by the specific classes as this
        requires LEFT JOIN.
        """

    def empty_form(self):
        """Create empty form for creating new item.  """
        item_data = {}
        for attr in self.attributes:
            item_data[attr] = ''

        if self.generate_id:
            item_id = self._gen_id()
            item_data[self.primary] = item_id

        return item_data

    def _gen_id(self):
        #sql=f'SELECT {self.primary} \
        #     FROM {self.table_name} \
        #     WHERE {self.primary} = ( \
        #         SELECT MAX(TO_NUMBER({self.primary}) DEFAULT NULL ON CONVERSION ERROR) \
        #         FROM {self.table_name} \
        #     )'
        sql = f'SELECT {self.primary} \
                FROM {self.table_name} \
                WHERE {self.primary} = ( \
                  SELECT MAX(TO_NUMBER({self.primary})) \
                  FROM {self.table_name} \
                )'
        data = DB.fetchall(DB.execute(DB.connect(), sql))
        if not data:
            item_id = 0
        else:
            item_id = int(data[0][0]) + 1
        return item_id

    def create(self, item_data: dict):
        """Create new entry.

        INSERT INTO GROUP5.TRACKUSER t
        ("userId",USERNAME,PASSWORD,SUPERVISORID,ADDERID)
        VALUES ('V00001','黃品堯','12345','','V00001')
        """
        # generate id if needed
        if self.generate_id:
            item_data[self.primary] = self._gen_id()

        sql = f'INSERT INTO GROUP5.{self.table_name} ('
        attr_sql = ''
        value_sql = ''
        for attr in self.attributes[:-1]:
            print(attr) # DEBUG
            # put None in absent attributes
            item_data[attr] = item_data.get(attr, None)
            print(item_data[attr]) # DEBUG
            print('-'*5) # DEBUG
            # set attributes
            attr_sql += f'"{attr}",'
            # set values
            value_sql += f':{attr},'
        attr_sql += f'"{self.attributes[-1]}")'
        value_sql += f':{self.attributes[-1]}) '

        sql += attr_sql
        sql += 'VALUES ('
        sql += value_sql

        DB.execute_input(DB.prepare(sql),
                         item_data)
        return item_data[self.primary]

    def edit(self, item_data: dict):
        """Update table entry.

        UPDATE group5.TRACKUSER SET ADDERID = 'V00001',username = '黃品堯'
        WHERE  "userId" = '0'
        """
        sql = f'UPDATE group5.{self.table_name} SET'

        for attr, value in list(item_data.items())[:-1]:
            sql += f'"{attr}" = '
            sql += f"'{value}',"
        sql += f'"{list(item_data.keys())[-1]}" = '
        sql += f"'{list(item_data.values())[-1]}' "
        sql += f'WHERE {self.primary} = {item_data[self.primary]}'
        DB.execute_input(DB.prepare(sql),
                         item_data)
        return item_data[self.primary]

    def save(self, item_data: dict):
        """Save data input by user.

        if user id exists, call edit user
        else call create_new_user
        """
        # TODO create new id if is none
        # check if item exists using primary key
        sql = f'SELECT COUNT(*) FROM GROUP5.{self.table_name}'
        sql += f' WHERE {self.primary} = '
        sql += f"'{item_data.get(self.primary, -1)}'"
        with DB.connect() as connection:
            # Execute the query with bind variables to prevent SQL injection
            count = connection.execute(sql).fetchone()[0]
        # call corresponding function
        if count:
            item_id = self.edit(item_data)
        else:
            item_id = self.create(item_data)

        return item_id

    def delete(self, item_id):
        sql = f'DELETE FROM GROUP5.{self.table_name} \
               WHERE {self.primary} = {item_id}'
        data = DB.execute(DB.connect(), sql)
        return
