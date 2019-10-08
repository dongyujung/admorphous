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
CREATE TABLE views_page_win AS
	SELECT
		document_id,
		WINDOWEND() AS window_end,
		CAST(count(*) AS int) AS count
	FROM pageviews
	WINDOW TUMBLING (SIZE 10 minutes)
	GROUP BY document_id;

CREATE TABLE views_page_win_filtered
    WITH (
        KAFKA_TOPIC='views_page_win_filtered',
        value_format='JSON'
    ) AS
	SELECT * FROM views_page_win
	WHERE count > 1;



