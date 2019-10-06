---------------------------------------------------------------
-- Count impressions of each ad (join & agg)
----------------------------------------------------------------

-- Events stream
CREATE STREAM events (
    display_id string,
    timestamp int
    )
	with (
	    KAFKA_TOPIC='events',
	    VALUE_FORMAT='JSON'
);

-- Display-ad mapping table
CREATE STREAM display_ad (
    display_id string,
    ad_id int
    )
	with (
	    KAFKA_TOPIC='display_ad',
	    VALUE_FORMAT='JSON'
);
