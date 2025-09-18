-- Create outbox_event table for product-validation-service
CREATE TABLE IF NOT EXISTS outbox_event (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data TEXT NOT NULL,
    topic VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processed_at TIMESTAMP,
    retry_count INTEGER NOT NULL DEFAULT 0,
    error_message TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_outbox_event_processed ON outbox_event (processed);
CREATE INDEX IF NOT EXISTS idx_outbox_event_created_at ON outbox_event (created_at);
CREATE INDEX IF NOT EXISTS idx_outbox_event_aggregate_id ON outbox_event (aggregate_id);