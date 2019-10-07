---------------------------------------------------------------
-- Count impressions of each ad (join & agg)
----------------------------------------------------------------

-- Events stream
CREATE STREAM events (
    display_id string
    )
	with (
	    KAFKA_TOPIC='events',
	    VALUE_FORMAT='JSON',
	    KEY='display_id'
);

-- Display-ad mapping stream
CREATE STREAM display_ad (
    display_id string,
    ad_id int
    )
	with (
	    KAFKA_TOPIC='display_ad',
	    VALUE_FORMAT='JSON',
	    KEY='display_id',
	    TIMESTAMP='map_time'
);

-- Join the events and display tables
CREATE STREAM impressions AS
	SELECT
		e.display_id AS display_id
		, e.event_time AS event_time
		, d.ad_id AS ad_id
	FROM events e
	JOIN display_ad d
	WITHIN 1 hour
	ON e.display_id = d.display_id;

-- Group by and count impressions for each ad
-- Automatically keyed as ad_id
CREATE TABLE impressions_ad
    WITH (KAFKA_TOPIC='impressions_ad', value_format='JSON') AS
	SELECT
		ad_id,
		cast(count(*) AS int) AS count,
		cast(max(event_time) AS BIGINT) AS last_ts
	FROM impressions
	GROUP BY ad_id;