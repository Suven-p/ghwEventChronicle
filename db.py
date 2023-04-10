import sqlite3
import json
import datetime

conn = sqlite3.connect('videos.db')


def setup():
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            stream_id TEXT,
            title TEXT,
            description TEXT,
            created_at TEXT,
            published_at TEXT,
            url TEXT,
            thumbnail_url TEXT,
            language TEXT,
            duration TEXT
        );
    ''')
    c.close()


def insert_video(video, cursor=None):
    if cursor is None:
        c = conn.cursor()
    else:
        c = cursor
    c.execute('''
        INSERT INTO videos (
            id,
            stream_id,
            title,
            description,
            created_at,
            published_at,
            url,
            thumbnail_url,
            language,
            duration
        ) VALUES (
            :id,
            :stream_id,
            :title,
            :description,
            :created_at,
            :published_at,
            :url,
            :thumbnail_url,
            :language,
            :duration
        ) ON CONFLICT(id) DO NOTHING;
    ''', video)
    if cursor is None:
        c.close()
        conn.commit()


def insert_from_json(filename):
    c = conn.cursor()
    with open(filename, 'r') as f:
        data = json.load(f)
    for video in data:
        insert_video(video, c)
    c.close()
    conn.commit()


def to_iso(date: str):
    if date.endswith('Z'):
        date.removesuffix('Z')
        date += '+00:00:00'
    return datetime.datetime.fromisoformat(date)


def get_probable_video(timestamp):
    c = conn.cursor()
    c.execute('''
        SELECT id, stream_id, title, created_at, url FROM videos
        WHERE created_at >= ?
        ORDER BY created_at
        LIMIT 1;
    ''', (timestamp,))
    video1 = c.fetchone()
    c.execute('''
        SELECT id, stream_id, title, created_at, url FROM videos
        WHERE created_at < ?
        ORDER BY created_at DESC
        LIMIT 1;
    ''', (timestamp,))
    video2 = c.fetchone()
    if not video1 and not video2:
        return None

    video = None
    diff1 = datetime.timedelta.max
    diff2 = datetime.timedelta.max
    if video1:
        video1_time = to_iso(video1[3])
        diff1 = abs(video1_time - to_iso(timestamp))
    if video2:
        video2_time = to_iso(video2[3])
        diff2 = abs(video2_time - to_iso(timestamp))
    if diff1 < diff2:
        video = video1
    else:
        video = video2
    video = {
        'id': video[0],
        'stream_id': video[1],
        'title': video[2],
        'created_at': video[3],
        'url': video[4],
    }
    c.close()
    return video


def main():
    setup()
    insert_from_json('user_videos.json')


if __name__ == '__main__':
    main()
