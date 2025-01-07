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
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  phone TEXT,
  password TEXT,
  created_at TIMESTAMP,
  client_id INT,
  UNIQUE (phone)
);

-- Schema for table stations
CREATE TABLE IF NOT EXISTS stations (
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
  published_at TIMESTAMP,
  client_id INT,
  station_id INT,
  UNIQUE (video_id, station_id)
);

-- Schema for table images from https://i.postimg.cc
CREATE TABLE IF NOT EXISTS postimg_images (
  id SERIAL PRIMARY KEY,
  image_id TEXT,
  published_at TIMESTAMP,
  client_id INT,
  station_id INT,
  UNIQUE (image_id, station_id)
);

-- Schema for table subscribers
CREATE TABLE IF NOT EXISTS subscribers (
  id SERIAL PRIMARY KEY,
  phone TEXT,
  created_at TIMESTAMP,
  station_id INT
);