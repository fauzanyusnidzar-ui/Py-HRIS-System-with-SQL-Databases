CREATE DATABASE hr_app;
SHOW DATABASES;
USE hr_app;
CREATE TABLE accounts (
    user_id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    role ENUM('user','supervisor','admin','super_admin') NOT NULL,
    blocked BOOLEAN DEFAULT FALSE,
    fail INT DEFAULT 0
);
INSERT INTO accounts (user_id, password, role)
VALUES 
('admin01','admin123','admin'),
('spv01','spv123','supervisor'),
('user01','user123','user'),
('super01','super123','super_admin');

SELECT * FROM accounts;

CREATE TABLE employees (
    nip VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(100),
    ttl VARCHAR(100),
    alamat_ktp VARCHAR(100),
    alamat_tinggal VARCHAR(100),
    hp VARCHAR(20),
    rumah VARCHAR(20),
    emergency VARCHAR(100),
    riwayat VARCHAR(100),
    pangkat VARCHAR(50),
    gaji INT,
    departemen VARCHAR(50)
);

CREATE TABLE resign_employees (
    nip VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(100),
    ttl VARCHAR(100),
    alamat_ktp VARCHAR(100),
    alamat_tinggal VARCHAR(100),
    hp VARCHAR(20),
    rumah VARCHAR(20),
    emergency VARCHAR(100),
    riwayat VARCHAR(100),
    pangkat VARCHAR(50),
    gaji INT,
    departemen VARCHAR(50)
);

SHOW TABLES;

DESCRIBE employees;
DESCRIBE accounts;

INSERT INTO employees 
(nip, nama, ttl, alamat_ktp, alamat_tinggal, hp, rumah, emergency, riwayat, pangkat, gaji, departemen)
VALUES
('1001','Alucard Dark Slayer','Land of Dawn, 12 Jan 1998','
Moniyan Empire','Castle of Light','081111001','02110001',
'Tigreal','Demon Hunter Squad','Officer',12000000,'Jungler'),
('1002','Miya Moonlight Archer','Moonlit Forest, 3 Mar 2000',
'Azrya Woodlands','Elven Base','081111002','02110002','Estes',
'Moon Elf Guard','Assistant',9500000,'Gold Lane'),
('1003','Chou Kungfu Master','Cadia Riverlands, 7 Jul 1997',
'Eastern Region','Dragon Temple','081111003','02110003','Ling',
'Martial Arts School','Senior Officer',13000000,'Roamer'),
('1004','Layla Energy Gunner','Eruditio, 1 Mei 2001','Scientific City',
'Tech District','081111004','02110004','Lolita','Energy Lab','Assistant',
9000000,'Gold Lane'),
('1005','Gusion Holy Blade','Paxley House, 9 Sep 1999','Magic Academy',
'Noble District','081111005','02110005','Aamon','Magic Assassin Guild',
'Officer',12500000,'Jungler');

SELECT * FROM employees;
INSERT INTO resign_employees
(nip, nama, ttl, alamat_ktp, alamat_tinggal, hp, rumah, emergency, 
riwayat, pangkat, gaji, departemen)
VALUES
('2001','Argus Fallen Angel','Moniyan Empire, 10 Okt 1996',
'Dark Abyss','Shadow Realm','082222001','02120001','Rafaela',
'Dark Forces','Officer',11000000,'EXP Lane'),
('2002','Hanzo Akuma Ninja','Scarlet Village, 5 Mei 1995',
'Cadia Riverlands','Forbidden Temple','082222002','02120002',
'Hanabi','Shadow Sect','Senior Officer',11500000,'Jungler');

SELECT * FROM resign_employees;
ALTER TABLE accounts
MODIFY blocked TINYINT(1) DEFAULT 0,
MODIFY fail INT DEFAULT 0,
MODIFY status VARCHAR(20) DEFAULT 'approved';
ALTER TABLE accounts 
MODIFY blocked TINYINT DEFAULT 0,
MODIFY fail INT DEFAULT 0;
SELECT * FROM accounts;
SELECT DATABASE();
USE hr_app;
SET SQL_SAFE_UPDATES = 0;
UPDATE accounts
SET status = 'approved'
WHERE status IS NULL;

SELECT * from accounts;
UPDATE accounts
SET blocked = 0;
USE hr_app;
SELECT * from accounts;
UPDATE accounts
SET fail = 0
WHERE user_id = 'user01';

SELECT * FROM accounts;

CREATE TABLE account_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_by VARCHAR(50) NOT NULL,
    target_user_id VARCHAR(50) NOT NULL,
    action ENUM('add','delete') NOT NULL,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SHOW TABLES;

DESCRIBE account_requests;

ALTER TABLE account_requests
ADD COLUMN password VARCHAR(255) NULL AFTER action;
ALTER TABLE account_requests
ADD COLUMN role ENUM('user','admin','supervisor') NULL AFTER action;
DESCRIBE account_requests;
SELECT * FROM account_requests;

