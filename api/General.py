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

    def create(self, item_data: dict):
        """Create new entry.

        INSERT INTO GROUP5.TRACKUSER t
        ("userId",USERNAME,PASSWORD,SUPERVISORID,ADDERID)
        VALUES ('V00001','黃品堯','12345','','V00001')
        """
        # generate id if needed
        if self.generate_id:
            sql=f'SELECT {self.primary} \
                 FROM {self.table_name} \
                 WHERE {self.primary} = ( \
                     SELECT MAX(TO_NUMBER({self.primary}) DEFAULT NULL ON CONVERSION ERROR) \
                     FROM {self.table_name} \
                 )'
            data = DB.fetchall(DB.execute(DB.connect(), sql))
            if not data:
                item_data[self.primary] = 0
            else:
                item_data[self.primary] = data[0][0] + 1

        sql = f'INSERT INTO GROUP5.{self.table_name} ('
        for attr in self.attributes[:-1]:
            # put None in absent attributes
            item_data[attr] = item_data.get(attr, None)
            # set attributes
            attr_sql += f'"{attr}",'
            # set values
            value_sql += f':{attr},'
        attr_sql += f'"{self.attributes[-1]}")'
        value_sql += f':{self.attributes[-1]})'

        sql += attr_sql
        sql += 'VALUES ('
        sql += value_sql

        DB.execute_input(DB.prepare(sql),
                         item_data)

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
        sql += f"'{list(item_data.values())[-1]}',"
        sql += 'WHERE "{self.primary}" = {item_data[self.primary]}'

    def save(self, item_data: dict):
        """Save data input by user.

        if user id exists, call edit user
        else call create_new_user
        """
        # TODO create new id if is none
        # check if item exists using primary key
        sql = 'SELECT COUNT(*) FROM GROUP5.{self.table_name}'
        sql += f' WHERE "{self.primary}" = '
        sql += "'{item_data[self.primary]}'"
        prepared_sql = DB.prepare(sql)
        count = DB.execute_input(prepared_sql)
        # call corresponding function
        if count:
            self.edit(item_data)
        else:
            self.create(item_data)
