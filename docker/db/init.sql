CREATE TABLE mailing (
    id SERIAL PRIMARY KEY,
    massege character varying(255),
    send_time timestamp with time zone,
    status  character varying(30)
);
CREATE TABLE user_answers (
    id SERIAL PRIMARY KEY,
    answer character varying(255) NOT NULL UNIQUE,
    mail_id character varying(255) NOT NULL,
    user_id character varying(255)
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    role character varying(255) NOT NULL UNIQUE,
    user_id bigint NOT NULL,
    user_name character varying(255)
);