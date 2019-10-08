---------------------------------------------------------------
-- Count impressions of each ad (join & agg)
----------------------------------------------------------------

-- Events stream
CREATE STREAM events (
    display_id string
    )
	with (
	    KAFKA_TOPIC='events',
	    VALUE_FORMAT='JSON'
);

-- Display-ad mapping stream
CREATE STREAM display_ad (
    display_id string,
    ad_id int
    )
	with (
	    KAFKA_TOPIC='display_ad',
	    VALUE_FORMAT='JSON'
);

-- Join the events and display tables
CREATE STREAM impressions AS
	SELECT
		e.display_id AS display_id
		, d.ad_id AS ad_id
	FROM events e
	JOIN display_ad d
	WITHIN 1 hour
	ON e.display_id = d.display_id;

-- Group by and count impressions for each ad
-- Automatically keyed as ad_id
CREATE TABLE impressions_ad AS
	SELECT
		ad_id,
		cast(count(*) AS int) AS count
	FROM impressions
	GROUP BY ad_id;

CREATE TABLE impressions_ad_filtered
    WITH (
        KAFKA_TOPIC='impressions_ad_filtered',
        value_format='JSON'
    ) AS
	SELECT * FROM impressions_ad
	WHERE count > 1;