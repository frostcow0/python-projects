CREATE DATABASE IF NOT EXISTS root_access;
USE root_access;

CREATE USER 'cmst'@'localhost' IDENTIFIED BY 'agroponics';

-- minLight may need changed depending what we do with our light sensor
CREATE TABLE environments (
    envId smallint NOT NULL,
    plant varchar(40),
    minMoist tinyint,
    PRIMARY KEY(envId)
);

CREATE TABLE sensor_data (
    id int NOT NULL AUTO_INCREMENT,
    envId smallint NOT NULL,
    whenCollected datetime NOT NULL, 
    timeLightOnMins smallint,
    humidity smallint,
    soilMoisture smallint,
    temperature smallint,
    waterConsumption smallint,
    PRIMARY KEY(id)
);

CREATE TABLE daily_metrics (
    id int NOT NULL, 
    envId smallint NOT NULL,
    dateProduced datetime NOT NULL,
    totalWaterConsumption smallint,
    totalTimeLightOnMins smallint,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS email_pass (
    email varchar(320) NOT NULL,
    pass varchar(40),
    PRIMARY KEY (email)
);

ALTER TABLE sensor_data
ADD FOREIGN KEY (envId) REFERENCES environments(envId);

ALTER TABLE daily_metrics
ADD FOREIGN KEY (envId) REFERENCES environments(envId);