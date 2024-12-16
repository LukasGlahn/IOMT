--@block

CREATE TABLE maskiner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL UNIQUE,
    IP VARCHAR(250) NOT NULL UNIQUE
);

--@block
SHOW TABLES;


--@block
INSERT INTO maskiner (name, IP) 
VALUES ('Machine5', '10.136.132.205');

--@block
SELECT * FROM maskiner

--@block
CREATE TABLE piller (
    Id INT NOT NULL PRIMARY KEY,
    name VARCHAR(250) NOT NULL UNIQUE
);

--@block
INSERT INTO piller (id, name) 
VALUES (2, "blå m&m");

--@block
SELECT * FROM piller