CREATE DATABASE IF NOT EXISTS logforge;

CREATE TABLE IF NOT EXISTS logforge.log_entries (
    id String,
    project_id String,
    source String,
    level String,
    message String,
    metadata String,
    traceback String,
    timestamp DateTime64(3, 'UTC')
) ENGINE = MergeTree()
ORDER BY (project_id, timestamp);
