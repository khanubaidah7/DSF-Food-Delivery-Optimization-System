create database if not exists Food_Delivery;
use Food_Delivery;
create table orders(
		id int auto_increment primary key,
        item_name varchar(100),
        price int,
        restaurant varchar(100),
        quantity int,
        total_price int,
        order_time timestamp default current_timestamp
);
select * from orders;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from users;