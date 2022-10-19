CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY,
    start_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS datasets (
    case_name VARCHAR(50) PRIMARY KEY,
    case_desc VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS wholeslides (
    uuid VARCHAR(50) PRIMARY KEY,
    fpath VARCHAR(50) NOT NULL,
    fname VARCHAR(50) NOT NULL,
    case_name VARCHAR(50) NOT NULL,
    FOREIGN KEY(case_name) references datasets(case_name),
    UNIQUE(fpath)
);
CREATE TABLE IF NOT EXISTS objects (
    slide_uuid VARCHAR(50) NOT NULL,
    fpath VARCHAR(50) NOT NULL ,
    file_type VARCHAR(50),
    file_desc VARCHAR(100),
    FOREIGN KEY(slide_uuid) references wholeslides(uuid),
    constraint PK PRIMARY KEY (slide_uuid, file_type)
);

