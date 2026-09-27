import os
import time
from datetime import datetime, timezone

import isodate
import pandas as pd
import requests
from dotenv import load_dotenv


# ==========================================
# CONFIGURAÇÕES
# ==========================================

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
HANDLE = os.getenv("YOUTUBE_HANDLE", "@dr.biogas")

BASE_URL = "https://www.googleapis.com/youtube/v3"


if not API_KEY:
    raise ValueError(
        "YOUTUBE_API_KEY não encontrada. "
        "Verifique seu arquivo .env."
    )


# ==========================================
# FUNÇÃO BASE PARA API
# ==========================================

def youtube_get(endpoint, params):
    params["key"] = API_KEY

    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        print("ERRO DA API:")
        print(response.text)

        response.raise_for_status()

    return response.json()


# ==========================================
# BUSCAR CANAL PELO HANDLE
# ==========================================

def get_channel(handle):

    data = youtube_get(
        "channels",
        {
            "part": "id,snippet,statistics,contentDetails",
            "forHandle": handle
        }
    )

    if not data.get("items"):
        raise ValueError(
            f"Canal não encontrado: {handle}"
        )

    channel = data["items"][0]

    return channel


# ==========================================
# PEGAR TODOS OS IDs DOS VÍDEOS
# ==========================================

def get_video_ids(playlist_id):

    video_ids = []
    page_token = None

    while True:

        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50
        }

        if page_token:
            params["pageToken"] = page_token

        data = youtube_get(
            "playlistItems",
            params
        )

        for item in data.get("items", []):

            video_id = (
                item
                .get("contentDetails", {})
                .get("videoId")
            )

            if video_id:
                video_ids.append(video_id)

        page_token = data.get("nextPageToken")

        print(
            f"Vídeos encontrados até agora: "
            f"{len(video_ids)}"
        )

        if not page_token:
            break

    return video_ids


# ==========================================
# CONVERTER DURAÇÃO
# ==========================================

def duration_seconds(duration):

    try:
        duration_obj = isodate.parse_duration(duration)
        return int(duration_obj.total_seconds())

    except Exception:
        return None


# ==========================================
# BUSCAR DADOS DOS VÍDEOS
# ==========================================

def get_video_details(video_ids):

    videos = []

    # Consulta em lotes
    for i in range(0, len(video_ids), 50):

        batch = video_ids[i:i + 50]

        data = youtube_get(
            "videos",
            {
                "part": "snippet,contentDetails,statistics",
                "id": ",".join(batch)
            }
        )

        for item in data.get("items", []):

            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})

            duration = content.get("duration")

            videos.append({

                "video_id":
                    item.get("id"),

                "url":
                    f"https://www.youtube.com/watch?v="
                    f"{item.get('id')}",

                "title":
                    snippet.get("title"),

                "description":
                    snippet.get("description"),

                "published_at":
                    snippet.get("publishedAt"),

                "category_id":
                    snippet.get("categoryId"),

                "tags":
                    " | ".join(
                        snippet.get("tags", [])
                    ),

                "thumbnail":
                    (
                        snippet
                        .get("thumbnails", {})
                        .get("high", {})
                        .get("url")
                    ),

                "duration_iso":
                    duration,

                "duration_seconds":
                    duration_seconds(duration),

                "views":
                    int(
                        stats.get(
                            "viewCount",
                            0
                        )
                    ),

                "likes":
                    int(
                        stats.get(
                            "likeCount",
                            0
                        )
                    ),

                "comments":
                    int(
                        stats.get(
                            "commentCount",
                            0
                        )
                    )
            })

        print(
            f"Detalhes processados: "
            f"{min(i + 50, len(video_ids))}"
            f"/{len(video_ids)}"
        )

        time.sleep(0.1)

    return videos


# ==========================================
# CRIAR MÉTRICAS
# ==========================================

def calculate_metrics(df):

    df["published_at"] = pd.to_datetime(
        df["published_at"],
        utc=True
    )

    now = pd.Timestamp.now(
        tz="UTC"
    )

    df["days_online"] = (
        now - df["published_at"]
    ).dt.total_seconds() / 86400

    df["days_online"] = (
        df["days_online"]
        .clip(lower=1)
    )

    df["duration_minutes"] = (
        df["duration_seconds"] / 60
    )

    df["views_per_day"] = (
        df["views"] /
        df["days_online"]
    )

    df["like_rate"] = (
        df["likes"] /
        df["views"]
        .replace(0, 1)
    )

    df["comment_rate"] = (
        df["comments"] /
        df["views"]
        .replace(0, 1)
    )

    df["engagement_rate"] = (
        (
            df["likes"] +
            df["comments"]
        )
        /
        df["views"].replace(0, 1)
    )

    df["published_weekday"] = (
        df["published_at"]
        .dt.day_name()
    )

    df["published_hour_utc"] = (
        df["published_at"]
        .dt.hour
    )

    return df


# ==========================================
# MAIN
# ==========================================

def main():

    print()
    print("==============================")
    print("YOUTUBE COMPETITOR INTELLIGENCE")
    print("==============================")
    print()

    print(
        f"Buscando canal: {HANDLE}"
    )

    channel = get_channel(HANDLE)

    channel_id = channel["id"]

    channel_name = (
        channel["snippet"]["title"]
    )

    statistics = (
        channel.get(
            "statistics",
            {}
        )
    )

    uploads_playlist = (
        channel
        ["contentDetails"]
        ["relatedPlaylists"]
        ["uploads"]
    )

    print()
    print(f"Canal: {channel_name}")
    print(f"ID: {channel_id}")
    print(
        "Inscritos:",
        statistics.get(
            "subscriberCount"
        )
    )
    print(
        "Visualizações:",
        statistics.get(
            "viewCount"
        )
    )
    print(
        "Vídeos:",
        statistics.get(
            "videoCount"
        )
    )

    print()
    print(
        "Buscando lista de vídeos..."
    )

    video_ids = get_video_ids(
        uploads_playlist
    )

    print()
    print(
        f"Total de vídeos: "
        f"{len(video_ids)}"
    )

    print()
    print(
        "Buscando métricas..."
    )

    videos = get_video_details(
        video_ids
    )

    df = pd.DataFrame(
        videos
    )

    df = calculate_metrics(
        df
    )

    df = df.sort_values(
        "views_per_day",
        ascending=False
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    timestamp = (
        datetime.now()
        .strftime(
            "%Y-%m-%d_%H-%M"
        )
    )

    output_path = (
        f"output/"
        f"youtube_{HANDLE.replace('@', '')}_"
        f"{timestamp}.csv"
    )

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print("==============================")
    print("CONCLUÍDO")
    print("==============================")

    print(
        f"Arquivo salvo em:"
    )

    print(
        output_path
    )

    print()

    print(
        "TOP 10 - VIEWS/DIA"
    )

    columns = [
        "title",
        "views",
        "views_per_day",
        "likes",
        "comments",
        "engagement_rate"
    ]

    print(
        df[columns]
        .head(10)
        .to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()