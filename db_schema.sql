-- Table structure for table clients
CREATE TABLE IF NOT EXISTS clients (
  id SERIAL PRIMARY KEY,
  name TEXT,
  youtubeChannelHandle TEXT,
  createdAt TIMESTAMP
);

-- Table structure for table stations
CREATE TABLE IF NOT EXISTS stations (
  id SERIAL PRIMARY KEY,
  name TEXT,
  routerIP TEXT,
  hotspotUsername TEXT,
  hotspotPassword TEXT,
  youtubeChannelHandle TEXT,
  createdAt TIMESTAMP,
  clientId INT
);

-- Table structure for table YouTube Videos
CREATE TABLE IF NOT EXISTS youtube_videos (
  id SERIAL PRIMARY KEY,
  videoId TEXT,
  publishedAt TIMESTAMP,
  clientId INT,
  stationId INT
);

-- Table structure for table https://i.postimg.cc images
CREATE TABLE IF NOT EXISTS postimg_images (
  id SERIAL PRIMARY KEY,
  imageId TEXT,
  publishedAt TIMESTAMP,
  clientId INT,
  stationId INT
);