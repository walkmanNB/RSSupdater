import json
import feedparser
from datetime import datetime

# 你可以把你的 RSS 源配置在这里，或者读取一个 opml/json 文件
SOURCES = [
    {"name": "大纪元新闻", "url": "https://feed.epochtimes.com/gb/feed", "type": "news"},
    {"name": "TED Radio Hour", "url": "https://feeds.npr.org/510298/podcast.xml", "type": "podcast"},
    {"name": "美国之音中文网", "url": "https://www.voachinese.com/api/zm_yql-vomx-tpeybti", "type": "news"},
    {"name": "美国之音中文广播", "url": "https://www.voachinese.com/api/zviqoyl-vomx-tpeugiov", "type": "podcast"},
    {"name": "无业游民", "url": "https://theue.me/feed/podcast?spm=5176.28158887.0.0.406dWzNLWzNLQr", "type": "podcast"},
    {"name": "少数派播客 SSPAI Podcast", "url": "https://sspai.typlog.io/feed/audio.xml?spm=5176.28158887.0.0.406dWzNLWzNLQr&file=audio.xml", "type": "podcast"}
]

all_items = []

for source in SOURCES:
    print(f"Fetching {source['name']}...")
    try:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:20]: # 每个源取前 20 条
            pub_date = entry.get('published', '')
            # 提取音频（播客）
            audio_url = ""
            if 'enclosures' in entry:
                for enc in entry.enclosures:
                    if 'audio' in enc.get('type', ''):
                        audio_url = enc.get('href', '')
            
            all_items.append({
                "title": entry.get('title', ''),
                "link": entry.get('link', ''),
                "description": entry.get('summary', '')[:200],
                "pubDate": pub_date,
                "audioUrl": audio_url,
                "sourceName": source['name'],
                "sourceType": source['type']
            })
    except Exception as e:
        print(f"Error parsing {source['name']}: {e}")

# 写入静态 JSON 文件
with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)

print("Successfully generated news.json")
