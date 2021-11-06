CREATE DATABASE IF NOT EXISTS root_access;
USE root_access;

-- minLight may need changed depending what we do with our light sensor
CREATE TABLE environments (
    envId smallint NOT NULL,
    plant varchar(40),
    maxTemp tinyint,
    minTemp tinyint,
    minLight smallint,
    maxHumid tinyint,
    minHumid tinyint,
    maxMoist tinyint,
    minMoist tinyint,
    PRIMARY KEY(envId)
);

CREATE TABLE sensor_data (
    id int NOT NULL,
    envId smallint NOT NULL,
    whenCollected datetime NOT NULL, 
    light smallint,
    humidity smallint,
    electricity smallint,
    soilMoisture smallint,
    temperature smallint,
    water smallint,
    PRIMARY KEY(id)
);

CREATE TABLE metrics (
    id int NOT NULL, 
    envId smallint NOT NULL,
    whenCollected datetime NOT NULL,
    avgElectricity smallint,
    growthElectricity smallint,
    growthWater smallint,
    moistureElectricity smallint,
    moistureWater smallint,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS email_pass (
    email varchar(40),
    pass varchar(40),
    PRIMARY KEY (email)
);

ALTER TABLE sensor_data
ADD FOREIGN KEY (envId) REFERENCES environments(envId);

ALTER TABLE metrics
ADD FOREIGN KEY (envId) REFERENCES environments(envId);