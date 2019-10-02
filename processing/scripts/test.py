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

platform_topic = app.topic('first-app-platform_table-changelog', value_type=int)
agg_count_topic = app.topic('agg_count_topic', value_type=PlatformCount)

@app.agent(pageview_topic)
async def aggregate_page_views(views):
    async for view in views.group_by(PageView.platform):
        platform_table[view.platform] += 1
        #platform_topic[] = view.platform
        #platform_topic["count"] = platform_table[view.platform]

@app.agent(platform_topic)
async def some_function(views_count):
    async for key, value in views_count.items():
        agg_count_topic[PlaformCount.platform] = key
        agg_count_topic[PlaformCount.count] = value