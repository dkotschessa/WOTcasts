from content_aggregator.settings.base import BASE_DIR

html_content = """

<html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<div>

 <link href="https://www.youtube.com/feeds/videos.xml?channel_id=ABCDEFG" rel="alternate" title="RSS" type="application/rss+xml"/>

</title>

<meta property="og:description" content="This is a description it is very exciting">

<div>


<p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>



</body>

</html>
"""


class SampleHtml:
    content = html_content
    response = 200


sample_html = SampleHtml


class SampleXML:
    test_xml = BASE_DIR / "podcasts" / "tests" / "sample.xml"
    content = open(test_xml).read()
    response = 200


sample_xml = SampleXML


class PodcastXML:
    test_xml = BASE_DIR / "podcasts" / "tests" / "dragon_podcast_xml.xml"
    content = open(test_xml).read()
    response = 200


podcast_xml = PodcastXML
