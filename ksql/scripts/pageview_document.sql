---------------------------------------------------------------
-- Count pageview of each webpage every 5 minutes
----------------------------------------------------------------

-- Source stream
CREATE STREAM upstream (pvid int,  uuid varchar, document_id varchar, timestamp int, platform string)
	with (KAFKA_TOPIC='upstream', VALUE_FORMAT='JSON');

-- Pageview count of each document for each tumbling window
-- Group by document_id and count pageviews in a tumbling window
CREATE TABLE tb_win_gb_count_doc WITH (KAFKA_TOPIC='tb_win_gb_count_doc', value_format='JSON') AS
	SELECT
		document_id,
		WINDOWEND() AS win_end,
		CAST(count(*) AS int) AS win_count,
		CAST(max(pvid) AS string) AS last_pvid
	FROM upstream
	WINDOW TUMBLING (SIZE 30 seconds)
	GROUP BY document_id;

-- Table to stream
CREATE STREAM st_win_gb_count_doc (document_id varchar, win_end bigint, win_count int, last_pvid bigint)
	with (KAFKA_TOPIC='tb_win_gb_count_doc', VALUE_FORMAT='JSON');

-- Rekey with last_pvid so that it can be joined with last_pvid later
CREATE STREAM st_win_gb_count_doc_rk AS
	SELECT * FROM st_win_gb_count_doc PARTITION BY last_pvid;


-- Pageview count of each document from beginning of time
-- Group by document_id and count pageviews no window
CREATE TABLE tb_gb_count_doc WITH (KAFKA_TOPIC='tb_gb_count_doc', value_format='JSON') AS \
	SELECT
		document_id,
		cast(count(*) AS int) AS agg_count,
		cast(max(pvid) AS string) AS last_pvid
	FROM upstream
	GROUP BY document_id;

-- Table to stream
CREATE STREAM st_gb_count_doc (document_id varchar, agg_count int, last_pvid bigint) \
	with (KAFKA_TOPIC='tb_gb_count_doc', VALUE_FORMAT='JSON');

-- Rekey with last_pvid so that it can be joined with last_pvid later
CREATE STREAM st_gb_count_doc_rk AS
	SELECT * FROM st_gb_count_doc PARTITION BY last_pvid;

-- Join the two streams on pageview id
CREATE STREAM st_joined1 AS
	SELECT
		l.last_pvid AS last_pvid
		, l.document_id AS document_id
		, l.win_end AS win_end
		, cast(l.win_count AS int) AS win_count
		, cast(r.agg_count AS int) AS agg_count
	FROM st_win_gb_count_doc_rk l
	JOIN st_gb_count_doc_rk r
	WITHIN 10 minutes
	ON l.last_pvid = r.last_pvid;

-- Join the two streams on pageview id
-- Duplicate as st_joined1
CREATE STREAM st_joined2 AS
	SELECT
		l.last_pvid AS last_pvid
		, l.document_id AS document_id
		, l.win_end AS win_end
		, cast(l.win_count AS int) AS win_count
		, cast(r.agg_count AS int) AS agg_count
	FROM st_win_gb_count_doc_rk l
	JOIN st_gb_count_doc_rk r
	WITHIN 10 minutes
	ON l.last_pvid = r.last_pvid;

-- Join the two identical joined streams
CREATE STREAM st_agg_filt_count_doc AS
	SELECT
		l.last_pvid AS last_pvid
		, TIMESTAMPTOSTRING(l.win_end, 'yyyy-MM-dd HH:mm:ss') AS win_end
		, l.document_id AS document_id
		, l.win_count AS win_count
		, l.agg_count AS agg_count
	FROM st_joined1 l
	JOIN st_joined2 r
	WITHIN 10 minutes
	ON l.document_id = r.document_id
	WHERE r.win_count = 1
	AND l.agg_count = r.agg_count - 1;
