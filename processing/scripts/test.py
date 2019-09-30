import faust

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

class Platform(faust.Record):
    platform: int
    count: int

page_view_topic = app.topic('test', value_type=PageView)

platform_table = app.Table('platform_table', default=int)
platform_topic = app.topic('platform', value_type=Platform)

@app.agent(page_view_topic)
async def count_page_views(views):
    async for view in views.group_by(PageView.platform):
        #platform_table["platform"] = view.platform
        #platform_table["count"] += 1
        platform_table[view.platform] += 1
        platform_topic["platform"] = view.platform
        platform_topic["count"] = platform_table[view.platform]


