GRANT ALL PRIVILEGES ON DATABASE delivery TO root;
CREATE TABLE IF NOT EXISTS delivery(
    id int not null primary key,
    num int not null,
    pdate date not null,
    priced float not null,
    pricer float not null
);