---------------------------------------------------------------
-- Count pageview of each webpage every 10 minutes
----------------------------------------------------------------

-- Source stream
CREATE STREAM upstream (
    pvid int,
    uuid varchar,
    document_id varchar,
    timestamp int,
    platform string
    )
	with (
	    KAFKA_TOPIC='pageviews',
	    VALUE_FORMAT='JSON'
);

-- Pageview count of each document for each tumbling window
-- Group by document_id and count pageviews in a tumbling window
CREATE TABLE tb_win_gb_count_doc WITH (KAFKA_TOPIC='tb_win_gb_count_doc', value_format='JSON') AS
	SELECT
		document_id,
		WINDOWEND() AS widow_end,
		CAST(count(*) AS int) AS win_count,
		CAST(max(pvid) AS string) AS last_pvid
	FROM upstream
	WINDOW TUMBLING (SIZE 10 minutes)
	GROUP BY document_id;

-- Table to stream
CREATE STREAM st_win_gb_count_doc (document_id varchar, win_end bigint, win_count int, last_pvid bigint)
	with (KAFKA_TOPIC='tb_win_gb_count_doc', VALUE_FORMAT='JSON');

