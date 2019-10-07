---------------------------------------------------------------
-- Count pageview of each webpage every 10 minutes
----------------------------------------------------------------

-- Source stream
CREATE STREAM pageviews (
    pvid int,
    document_id varchar,
    pageview_time BIGINT
    )
	with (
	    KAFKA_TOPIC='pageviews',
	    VALUE_FORMAT='JSON',
	    TIMESTAMP='pageview_time'
);

-- Pageview count of each document for each tumbling window
-- Group by document_id and count pageviews in a tumbling window
CREATE TABLE views_page_win WITH (
    KAFKA_TOPIC='views_page_win',
    value_format='JSON'
    ) AS
	SELECT
		document_id,
		WINDOWEND() AS window_end,
		CAST(count(*) AS int) AS count,
		CAST(max(pvid) AS int) AS last_pvid
	FROM pageviews
	WINDOW TUMBLING (SIZE 10 minutes)
	GROUP BY document_id;



