import faust
from datetime import timedelta

app = faust.App(
    'first-app',
    broker='kafka://localhost:9092',
    topic_partitions=1,
    value_serializer='json'
)


class PageView(faust.Record):
    uuid: str
    document_id: int
    timestamp: int
    platform: int
    geo_location: str
    traffic_source: int


class PlatformCount(faust.Record):
    platform: int
    count: int


pageview_topic = app.topic('upstream', value_type=PageView)

platform_table = app.Table('platform_table', default=int).tumbling(
    timedelta(minutes=1),
    expires=timedelta(hours=1),
)

platform_topic = app.topic('first-app-platform_table-changelog', value_type=PageView)

@app.agent(pageview_topic)
async def aggregate_page_views(views):
    async for view in views:
        platform_table[view] += 1
        #platform_topic["platform"] = view.platform
        #platform_topic["count"] = platform_table[view.platform]

