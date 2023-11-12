from link import *
class Filter():
    def __init__(self):
        self.user = '%'
        self.status = '%'
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

