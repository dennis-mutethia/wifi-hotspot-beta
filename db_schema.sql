
-- Schema for table users
CREATE TABLE IF NOT EXISTS system_users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  phone TEXT,
  password TEXT,
  created_at TIMESTAMP,
  client_id INT,
  UNIQUE (phone)
);

-- Schema for table clients
CREATE TABLE IF NOT EXISTS clients (
  id SERIAL PRIMARY KEY,
  name TEXT,
  phone TEXT,
  background_color TEXT,
  foreground_color TEXT,
  created_at TIMESTAMP
);

-- Schema for table hotspots
CREATE TABLE IF NOT EXISTS hotspots (
  id SERIAL PRIMARY KEY,
  name TEXT,
  hotspot_username TEXT,
  hotspot_password TEXT,
  created_at TIMESTAMP,
  client_id INT
);

-- Schema for table media
CREATE TABLE IF NOT EXISTS media (
  id SERIAL PRIMARY KEY,
  type TEXT NOT NULL,
  source_id TEXT,
  client_id INT,
  hotspot_id INT,
  UNIQUE (type, source_id, hotspot_id)
);

-- Schema for table subscribers
CREATE TABLE IF NOT EXISTS subscribers (
  id SERIAL,
  phone TEXT NOT NULL,
  session_hour TIMESTAMP NOT NULL,
  client_id INT,
  hotspot_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (phone, session_hour, hotspot_id)
);

