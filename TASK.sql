CREATE TABLE TRACKUSER
(
    userId CHAR(8) NOT NULL,
    userName VARCHAR(255) NOT NULL,
    password VARCHAR(50) NOT NULL,
    supervisorId CHAR(8),
    adderId CHAR(8) NOT NULL,
    PRIMARY KEY (userId),
    FOREIGN KEY (supervisorId) REFERENCES TRACKUSER(userId),
    FOREIGN KEY (adderId) REFERENCES TRACKUSER(userId)
);

CREATE TABLE TASK
(
    taskId CHAR(8) NOT NULL,
    status VARCHAR(20) NOT NULL,
    description NVARCHAR(MAX),
    taskOwner CHAR(8),
    title CHAR(20),
    dueDate DATETIME,
    assigner CHAR(8),
    creator CHAR(8) NOT NULL,
    assignTime DATETIME,
    PRIMARY KEY (taskId),
    FOREIGN KEY (taskOwner) REFERENCES TRACKUSER(userId),
    FOREIGN KEY (assigner) REFERENCES TRACKUSER(userId),
    FOREIGN KEY (creator) REFERENCES TRACKUSER(userId)
);

CREATE TABLE TASKCOMMENT
(
    commentId CHAR(8) NOT NULL,
    commenterId CHAR(8) NOT NULL,
    taskId CHAR(8) NOT NULL,
    content NVARCHAR(MAX) NOT NULL,
    commentTime DATETIME NOT NULL,
    lastUpdateTime DATETIME,
    PRIMARY KEY (commentId),
    FOREIGN KEY (commenterId) REFERENCES TRACKUSER(userId),
    FOREIGN KEY (taskId) REFERENCES TASK(taskId)
);