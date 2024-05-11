DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE awnsers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  problem TEXT NOT NULL,
  user_awnser BOOLEAN NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

create table user_options
(
    id                       INTEGER
        primary key autoincrement,
    author_id                INTEGER not null
        references user,
    operator_plus_option     BOOLEAN not null,
    operator_minus_option    BOOLEAN,
    operator_multiply_option BOOLEAN
);
