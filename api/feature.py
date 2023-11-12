from link import *
from api.General import General
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
    def __init__(self, item_id):
        self.featureId = item_id
        self.table_name = "FEATURE"
        self.attributes = ["featureId", "creatorId", "maintainerId", "title",
                           "description"]
        self.primary = "featureId"

    def list_features(self, featureId, keyword):
        sql = 'SELECT f.*, \
                      u_creator.userName as creatorName, \
                      u_maintainer.userName as maintainerName, \
               FROM FEATURE AS f \
               LEFT JOIN TRACKUSER AS u_creator ON f.creatorId = u_creator."userId" \
               LEFT JOIN TRACKUSER AS u_maintainer ON t.maintainerId = u_maintainer."userId"'
        sql += "WHERE (f.title LIKE '%:keyword%' \
                OR f.description LIKE '%:keyword%') \
                AND f.featureId LIKE '%:featureId%"
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'keyword': keyword,
                                             'featureId': featureId}))


    def get_details(self):
        sql = 'SELECT f.*, \
                      u_creator.userName as creatorName, \
                      u_maintainer.userName as maintainerName, \
               FROM FEATURE AS f \
               LEFT JOIN TRACKUSER AS u_creator ON f.creatorId = u_creator."userId" \
               LEFT JOIN TRACKUSER AS u_maintainer ON t.maintainerId = u_maintainer."userId" \
               WHERE f.featuerId = :featureId'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'featureId': self.featureId}))

    def list_tasks(self):
        """Get details of feature.

        Returns:
        - all details of tasks belonging to this feature
        """
        sql = "SELECT t.*, \
               FROM FEATURE AS f, \
               LEFT JOIN FEATURETASKRELATION AS r ON f.featureId = r.featureId \
               LEFT JOIN TASK AS t ON r.taskId = t.taskId \
               WHERE f.featureId = :featureId"
        return DB.fetchall(DB.execute_input(DB.prepare(sql),
                                            {'featureid': self.featureId}))

