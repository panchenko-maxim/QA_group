DROP TABLE Order_;
DROP TABLE Place;
DROP TABLE Status_order;
DROP TABLE Client;
DROP TABLE Cart;
DROP TABLE Size;
DROP TABLE Photobank;
DROP TABLE Shoes;


DELETE FROM Shoes
WHERE id=1;

INSERT INTO Shoes(shoes_code) VALUES(3568); 

SELECT MAX(id) AS max_id
FROM Shoes;

INSERT INTO Shoes(shoes_code) VALUES(2535) WHERE id=1;