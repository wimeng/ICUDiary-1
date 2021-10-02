PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username VARCHAR(20) PRIMARY KEY,
  firstname VARCHAR(20) NOT NULL,
  lastname VARCHAR(20) NOT NULL,
  email VARCHAR(40) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  password VARCHAR(256) NOT NULL,
  patient VARCHAR(20) NOT NULL,
  role VARCHAR(30) NOT NULL,
  PRIMARY KEY(username)
);

CREATE TABLE entries(
  entryid INTEGER NOT NULL,
  filename VARCHAR(64) NOT NULL,
  writer VARCHAR(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(entryid),
  FOREIGN KEY(writer) REFERENCES users(username) ON DELETE CASCADE
);

