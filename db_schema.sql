-- Schema for table clients
CREATE TABLE IF NOT EXISTS clients (
  id SERIAL PRIMARY KEY,
  name TEXT,
  backgroundColor TEXT,
  foregroundColor TEXT,
  createdAt TIMESTAMP
);

-- Schema for table users
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  phone TEXT,
  password TEXT,
  createdAt TIMESTAMP,
  clientId INT,
  UNIQUE (phone)
);

-- Schema for table stations
CREATE TABLE IF NOT EXISTS stations (
  id SERIAL PRIMARY KEY,
  name TEXT,
  hotspotUsername TEXT,
  hotspotPassword TEXT,
  createdAt TIMESTAMP,
  clientId INT
);

-- Schema for table YouTube Videos
CREATE TABLE IF NOT EXISTS youtube_videos (
  id SERIAL PRIMARY KEY,
  videoId TEXT,
  videoTitle TEXT,
  publishedAt TIMESTAMP,
  clientId INT,
  stationId INT,
  UNIQUE (videoId, stationId)
);

-- Schema for table https://i.postimg.cc images
CREATE TABLE IF NOT EXISTS postimg_images (
  id SERIAL PRIMARY KEY,
  imageId TEXT,
  publishedAt TIMESTAMP,
  clientId INT,
  stationId INT,
  UNIQUE (imageId, stationId)
);