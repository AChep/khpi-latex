CREATE TABLE category (
  cat_id INTEGER PRIMARY KEY,
  cat_name VARCHAR NOT NULL
);
CREATE TABLE product (
  pro_id INTEGER PRIMARY KEY,
  cat_id INTEGER REFERENCES category NOT NULL,
  pro_name VARCHAR NOT NULL,
  pro_description VARCHAR,
  pro_price REAL NOT NULL,
  pro_unit VARCHAR,
  pro_image VARCHAR,
  pro_state INTEGER NOT NULL
);
CREATE TABLE user (
  usr_id INTEGER PRIMARY KEY,
  usr_email VARCHAR NOT NULL,
  usr_phone VARCHAR NOT NULL,
  usr_secret VARCHAR NOT NULL,
  usr_group INTEGER NOT NULL,
  CONSTRAINT usr_email_unique UNIQUE (usr_email)
);
;
CREATE TABLE ordr (
  ord_id INTEGER PRIMARY KEY,
  usr_id INTEGER REFERENCES user NOT NULL,
  ord_date_created INTEGER NOT NULL,
  ord_date_archived INTEGER,
  ord_paid INTEGER NOT NULL 
);
CREATE TABLE product_ordr (
  pro_id INTEGER REFERENCES product ,
  ord_id INTEGER REFERENCES ordr,
  poa_quantity INTEGER NOT NULL,
  poa_price REAL NOT NULL,
  PRIMARY KEY (pro_id, ord_id)
);
