CREATE TABLE Group5.TRACKUSER
(
    "userId" CHAR(8) PRIMARY KEY,
    userName VARCHAR2(255) NOT NULL,
    password VARCHAR2(50) NOT NULL,
    supervisorId CHAR(8),
    adderId CHAR(8) NOT NULL,
    FOREIGN KEY (supervisorId) REFERENCES Group5.TRACKUSER("userId"),
    FOREIGN KEY (adderId) REFERENCES Group5.TRACKUSER("userId")
);

CREATE TABLE Group5.Task
(
    "taskId" CHAR(8) PRIMARY KEY,
    status VARCHAR2(20) NOT NULL,
    description CLOB,
    taskOwner CHAR(8),
    title VARCHAR2(20),
    dueDate TIMESTAMP,
    assigner CHAR(8),
    creator CHAR(8) NOT NULL,
    assignTime TIMESTAMP,
    FOREIGN KEY (taskOwner) REFERENCES Group5.TRACKUSER("userId"),
    FOREIGN KEY (assigner) REFERENCES Group5.TRACKUSER("userId"),
    FOREIGN KEY (creator) REFERENCES Group5.TRACKUSER("userId")
);

CREATE TABLE Group5.TASKCOMMENT
(
    commentId CHAR(8) PRIMARY KEY,
    commenterId CHAR(8) NOT NULL,
    taskId CHAR(8) NOT NULL,
    content CLOB NOT NULL,
    commentTime TIMESTAMP NOT NULL,
    lastUpdateTime TIMESTAMP,
    FOREIGN KEY (commenterId) REFERENCES Group5.TRACKUSER("userId"),
    FOREIGN KEY (taskId) REFERENCES Group5.Task("taskId")
);


CREATE TABLE group5.Feature
(
    featureId CHAR(8) PRIMARY KEY,
    creatorId CHAR(8) NOT NULL,
    maintainerId CHAR(8) NOT NULL,
    title VARCHAR2(20),
    description CLOB NOT NULL,
    FOREIGN KEY (creatorId) REFERENCES GROUP5.TRACKUSER("userId"),
    FOREIGN KEY (maintainerId) REFERENCES GROUP5.TRACKUSER("userId")
);

CREATE TABLE FeatureTaskRelation
(
    featureId CHAR(8) NOT NULL,
    taskId CHAR(8) NOT NULL,
    taskOrder INT,
    FOREIGN KEY (featureId) REFERENCES group5.Feature(featureId),
    FOREIGN KEY (taskId) REFERENCES group5.Task("taskId")
);
