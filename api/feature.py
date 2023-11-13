from link import *
from api.General import General
from api.sql import DB
from api.task import Task
class Feature(General):
    """Similar to task, but describes the features required.

    A feature may have multiple tasks, and a task may belong to none, one,
    or multiple features.
    One can note the order of which the tasks belonging to a feature have to be
    done; the order can duplicate as two tasks can be done at the same time
    without gating one another.

    Attributes:
      featureId: the id of the feature
      creatorId: the person who created this feature
      maintainerId: the person responsible for maintaining the feature
      title: feature title
      description: feature description
    """
    def __init__(self, item_id = None):
        self.featureId = item_id
        self.table_name = "FEATURE"
        self.attributes = ["featureId", "creatorId", "maintainerId", "title",
                           "description"]
        self.primary = "featureId"
        self.list_page = "viewfeature.html"
        self.detail_page = "featuredetail.html"
        self.generate_id = True

    def list_items(self, featureId = '%', keyword = ''):
        title = self.attributes.copy()
        title.extend(["creatorName", "maintainerName"])
        sql = 'SELECT f.*, \
                      u_creator.userName creatorName, \
                      u_maintainer.userName maintainerName \
               FROM FEATURE f \
               LEFT JOIN TRACKUSER u_creator ON f.creatorId = u_creator."userId" \
               LEFT JOIN TRACKUSER u_maintainer ON f.maintainerId = u_maintainer."userId"'
        #sql += "WHERE (f.title LIKE '%{keyword}%' \
        #        OR f.description LIKE '%{keyword}%') \
        #        AND f.featureId LIKE '{featureId}'"
        data = DB.fetchall(DB.execute(DB.connect(), sql))
        data_list = []
        for entry in data:
            data_list.append(dict(zip(title, entry)))
        return data_list


    def get_details(self, featureId):
        title = self.attributes.copy()
        title.extend(["creatorName", "maintainerName"])
        sql = 'SELECT f.*, \
                      u_creator.userName creatorName, \
                      u_maintainer.userName maintainerName, \
               FROM FEATURE f \
               LEFT JOIN TRACKUSER u_creator ON f.creatorId = u_creator."userId" \
               LEFT JOIN TRACKUSER u_maintainer ON t.maintainerId = u_maintainer."userId" \
               WHERE f.featuerId = :featureId'
        data = DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'featureId': featureId}))
        return dict(zip(title, data[0]))

    def list_tasks(self):
        """Get details of feature.

        Returns:
        - all details of tasks belonging to this feature
        """
        title = Task().attributes.copy()
        title.append('ownerName')
        sql = "SELECT t.*, u_owner.userName ownerName \
               FROM FEATURE f, \
               LEFT JOIN FEATURETASKRELATION r ON f.featureId = r.featureId \
               LEFT JOIN TASK t ON r.taskId = t.taskId "
        sql+=  'LEFT JOIN TRACKUSER u_owner ON t.taskOwner = u_owner."userId" \
               WHERE f.featureId = :featureId'
        data = DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'featureid': self.featureId}))
        data_list = []
        for entry in data:
            data_list.append(dict(zip(title, data[0])))
        return data_list
