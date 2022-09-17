CREATE TABLE IF NOT EXISTS wholeslides (
    uuid VARCHAR(30) PRIMARY KEY,  
    alias VARCHAR(30)
);


CREATE TABLE IF NOT EXISTS files (
    uuid VARCHAR(30),
    fname VARCHAR(30) NOT NULL,
    fext VARCHAR(10) NOT NULL,
    FOREIGN KEY(uuid) REFERENCES wholeslides(uuid),
    PRIMARY KEY (uuid, fext)
)