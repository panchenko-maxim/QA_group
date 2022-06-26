CREATE TABLE Shoes(
    id INT PRIMARY KEY,
    shoes_code INT UNIQUE,
    active BOOLEAN,
    description VARCHAR(250),
    measurements VARCHAR(100),
    sale INTEGER,
    wholesale INTEGER,
    retail INTEGER
);

CREATE TABLE Photobank(
    id INT PRIMARY KEY,
    link VARCHAR(100),
    shoes_id INT REFERENCES Shoes(id),
    number INTEGER
);

CREATE TABLE Size(
    id INT PRIMARY KEY,
    shoes_id INT REFERENCES Shoes(id),
    size INTEGER,
    foot_cm FLOAT,
    quantity INTEGER
);

CREATE TABLE Cart(
    id INT PRIMARY KEY
);

CREATE TABLE Client(
    id INT PRIMARY KEY, -- chat id
    username VARCHAR(30),
    information VARCHAR(100) NULL,
    contact VARCHAR(30) NULL,
    balance INTEGER NULL,
    active_cart_id INT REFERENCES Cart(id),
    bot_message_id INT NULL,
    next_message_handler INT NULL,    -- index of handler in list
    shoes_id_active INT NULL,
    shoes_position_for_change VARCHAR(30) NULL
);

CREATE TABLE Status_order(
    id INT PRIMARY KEY,
    status VARCHAR(20)
);

CREATE TABLE Place(
    id INT PRIMARY KEY,
    shoes_id INT REFERENCES Shoes(id),
    size INTEGER,
    cart_id REFERENCES Cart(id)
);

CREATE TABLE Order_(
    id INT PRIMARY KEY,
    cart_id INT REFERENCES Cart(id),
    datetime TIMESTAMP CURRENT_TIMESTAMP,
    status_order_id INT REFERENCES Status_order(id),
    client_id INT REFERENCES Client(id)
);
