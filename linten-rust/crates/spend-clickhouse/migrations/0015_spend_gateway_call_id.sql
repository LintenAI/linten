ALTER TABLE {database}.spend_logs
    ADD COLUMN IF NOT EXISTS linten_call_id String DEFAULT '' AFTER response_id,
    ADD INDEX IF NOT EXISTS idx_linten_call_id linten_call_id
        TYPE bloom_filter(0.001) GRANULARITY 1,
    ADD INDEX IF NOT EXISTS idx_request_id request_id
        TYPE bloom_filter(0.001) GRANULARITY 1
