PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username VARCHAR(20) PRIMARY KEY,
  firstname VARCHAR(20) NOT NULL,
  lastname VARCHAR(20) NOT NULL,
  email VARCHAR(40) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  password VARCHAR(256) NOT NULL,
  role VARCHAR(30) NOT NULL
);

CREATE TABLE superuser(
  username VARCHAR(20) PRIMARY KEY,
  superusercode VARCHAR(20) NOT NULL,
  has_perms BOOLEAN NOT NULL CHECK (has_perms IN (0, 1)) DEFAULT 1,
  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE table patient(
  username VARCHAR(20),
  patientcode VARCHAR(20) NOT NULL,
  notifcount INTEGER,
  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE text_entries(
  entryid INTEGER PRIMARY KEY,
  entryname VARCHAR(100) NOT NULL,
  entrytext VARCHAR(500) NOT NULL,
  writer VARCHAR(20) NOT NULL,
  patient VARCHAR(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  transcription VARCHAR(1000),
  FOREIGN KEY(writer) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE audio_entries(
  entryid INTEGER PRIMARY KEY,
  entryname VARCHAR(100) NOT NULL,
  entryaudio VARCHAR(250) NOT NULL,
  writer VARCHAR(20) NOT NULL,
  patient VARCHAR(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  transcription VARCHAR(1000) NOT NULL,
  FOREIGN KEY(writer) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE entries(
  entryid INTEGER PRIMARY KEY,
  entryname VARCHAR(100) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  writer VARCHAR(20) NOT NULL,
  patient VARCHAR(20) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(writer) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE security_question(
  question VARCHAR(20) NOT NULL,
  answer VARCHAR(20) NOT NULL,
  user VARCHAR(20) NOT NULL,
  FOREIGN KEY(user) REFERENCES users(username) ON DELETE CASCADE
);

