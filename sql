CREATE TABLE users (
    username VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(10) NOT NULL,
    cognome VARCHAR(10) NOT NULL,
    password VARCHAR(10) NOT NULL
);
CREATE TABLE posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(10),
    caption VARCHAR(255),
    image_url VARCHAR(255),
    FOREIGN KEY (username) REFERENCES users(username)
);
