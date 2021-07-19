-- noinspection SqlNoDataSourceInspectionForFile

DROP TABLE IF EXISTS experiments;

CREATE TABLE experiments (
    _id integer PRIMARY KEY AUTOINCREMENT,
    hash text NOT NULL,
    length real NOT NULL,
    start_pos real NOT NULL,
    T_min real NOT NULL,
    T_max real NOT NULL,
    T_rear real NOT NULL,
    duration real NOT NULL,
    frames_per_sec real NOT NULL,
    simulation_type text NOT NULL,
    n_flies integer NOT NULL,
    date_submit text NOT NULL,
    date_start text,
    date_finish text
);
