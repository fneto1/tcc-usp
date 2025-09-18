-- Migration script for creating outbox_event table in inventory-service

CREATE TABLE IF NOT EXISTS outbox_event (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    event_data TEXT NOT NULL,
    destination VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processed_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT
);

-- Index for better performance when querying unprocessed events
CREATE INDEX IF NOT EXISTS idx_outbox_event_processed_created_at
ON outbox_event (processed, created_at)
WHERE processed = FALSE;

-- Index for retry limit queries
CREATE INDEX IF NOT EXISTS idx_outbox_event_processed_retry_count
ON outbox_event (processed, retry_count, created_at)
WHERE processed = FALSE;