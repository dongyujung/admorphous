import faust

app = faust.App(
    'first-app',
    broker='kafka://localhost:9092',
    topic_partitions=1,
)

class PageView(faust.Record):
    uuid: str
    document_id: int
    timestamp: int
    platform: int
    geo_location: str
    traffic_source: int

page_view_topic = app.topic('test', value_type=PageView)

page_views_table = app.Table('page_views', default=int)

@app.agent(pageview_topic)
async def count_page_views(views):
    async for view in views.group_by(PageView.platform):
        page_views_table[view.platform] += 1

