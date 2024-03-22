CREATE TABLE urls (
        id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        name varchar(255) UNIQUE NOT NULL,
        created_at timestamp
);


CREATE TABLE url_checks (
        id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        url_id integer REFERENCES urls(id),
        status_code bigint, 
        h1 varchar,
        title text,
        description text,
        created_at timestamp
);
