CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    account NVARCHAR(255) UNIQUE NOT NULL,
    type_user NVARCHAR(50) NOT NULL,
    type_broker NVARCHAR(50),
    type_client NVARCHAR(50), 
    password NVARCHAR(255) NOT NULL
);

CREATE TABLE fake_data (
    id INT IDENTITY(1,1) PRIMARY KEY,
    account NVARCHAR(255) NOT NULL,
    data NVARCHAR(MAX) NOT NULL,
    FOREIGN KEY (account) REFERENCES users(account) ON DELETE CASCADE
);