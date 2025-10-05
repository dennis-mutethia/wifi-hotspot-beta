-- Schema for table clients
CREATE TABLE IF NOT EXISTS clients (
  id SERIAL PRIMARY KEY,
  name TEXT,
  phone TEXT,
  background_color TEXT,
  foreground_color TEXT,
  created_at TIMESTAMP
);

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

-- Schema for table hotspots
CREATE TABLE IF NOT EXISTS hotspots (
  id SERIAL PRIMARY KEY,
  name TEXT,
  hotspot_username TEXT,
  hotspot_password TEXT,
  created_at TIMESTAMP,
  client_id INT
);

-- Schema for table YouTube Videos
CREATE TABLE IF NOT EXISTS youtube_videos (
  id SERIAL PRIMARY KEY,
  video_id TEXT,
  video_title TEXT,
  client_id INT,
  hotspot_id INT,
  UNIQUE (video_id, hotspot_id)
);

-- Schema for table images from https://i.postimg.cc
CREATE TABLE IF NOT EXISTS postimg_images (
  id SERIAL PRIMARY KEY,
  image_id TEXT,
  client_id INT,
  hotspot_id INT,  
  UNIQUE (image_id, hotspot_id)
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

