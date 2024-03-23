CREATE TABLE tasks (
    task_id SERIAL NOT NULL,
    name VARCHAR (255) NOT NULL,
    majorClass VARCHAR (255) NOT NULL,
    minorClass VARCHAR (255) NOT NULL,
    have_interval BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    PRIMARY KEY (task_id)
);

CREATE TABLE intervals (
    interval_id SERIAL NOT NULL,
    task_id SERIAL,
    interval INT NOT NULL,
    PRIMARY KEY (interval_id),
    FOREIGN KEY (task_id) REFERENCES tasks (task_id)
);

CREATE TABLE weekdays (
    weekday_id SERIAL NOT NULL,
    task_id SERIAL,
    day_of_week VARCHAR (5) NOT NULL,
    PRIMARY KEY (weekday_id),
    FOREIGN KEY (task_id) REFERENCES tasks (task_id)
);

CREATE TABLE histories (
    history_id SERIAL NOT NULL,
    task_id SERIAL,
    updated_by VARCHAR (10) NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (history_id),
    FOREIGN KEY (task_id) REFERENCES tasks (task_id)
);

CREATE TABLE processes (
    process_id SERIAL NOT NULL,
    task_id SERIAL,
    process_number INT NOT NULL,
    operation VARCHAR (255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (process_id),
    FOREIGN KEY (task_id) REFERENCES tasks (task_id)
);
