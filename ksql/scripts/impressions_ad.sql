---------------------------------------------------------------
-- Count impressions of each ad (join & agg)
----------------------------------------------------------------

-- Events stream
CREATE STREAM events (
    display_id string
    timestamp BIGINT
    )
	with (
	    KAFKA_TOPIC='events',
	    VALUE_FORMAT='JSON'
);

-- Display-ad mapping stream
CREATE STREAM display_ad (
    display_id string,
    ad_id string
    )
	with (
	    KAFKA_TOPIC='display_ad',
	    VALUE_FORMAT='JSON'
);

-- Join the events and display tables
CREATE STREAM impressions AS
	SELECT
		e.display_id AS display_id
		e.timestamp AS event_ts
		, d.ad_id AS ad_id
	FROM events e
	JOIN display_ad d
	WITHIN 1 hour
	ON e.display_id = d.display_id;

-- Group by and count impressions for each ad
-- Automatically keyed as ad_id
CREATE TABLE impressions_ad with (
	    KAFKA_TOPIC='t_impressions_ad',
	    VALUE_FORMAT='JSON'
    ) AS
	SELECT
		ad_id,
		max(ROWTIME),
		cast(count(*) AS int) AS count
	FROM impressions
	GROUP BY ad_id;

-- Table to stream
CREATE STREAM st_impressions_ad (
    ad_id string,
    count int)
	with (
	    KAFKA_TOPIC='t_impressions_ad',
	    VALUE_FORMAT='JSON'
);

-- Filtered Stream
CREATE STREAM impressions_ad_filtered AS
	SELECT * FROM st_impressions_ad
	WHERE count > 1;