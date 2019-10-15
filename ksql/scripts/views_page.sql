---------------------------------------------------------------
-- Count pageview of each webpage every 10 minutes
----------------------------------------------------------------

-- Source stream
create STREAM pageviews (
    pvid int,
    document_id string
    )
	with (
	    KAFKA_TOPIC='pageviews',
	    VALUE_FORMAT='JSON'
);

-- Pageview count of each document for each tumbling window
-- Group by document_id and count pageviews in a tumbling window
CREATE TABLE t_views_page_win
    with (
	    KAFKA_TOPIC='t_views_page_win',
	    VALUE_FORMAT='JSON'
    ) AS
	SELECT
		document_id,
		CAST(count(*) AS int) AS count,
		WINDOWEND() AS win_end
	FROM pageviews
	WINDOW TUMBLING (SIZE 10 minutes)
	GROUP BY document_id;

-- Table to stream
CREATE STREAM st_views_page_win (
    document_id string,
    count int,
    win_end bigint
    )
	with (
	    KAFKA_TOPIC='t_views_page_win',
	    VALUE_FORMAT='JSON'
);

CREATE STREAM views_page_win_filtered AS
	SELECT * FROM st_views_page_win
	WHERE count > 1;



