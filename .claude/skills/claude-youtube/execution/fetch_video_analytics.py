"""
Fetch private video analytics from YouTube Analytics API.

Requires OAuth 2.0 authentication. Can ONLY access analytics for channels
you own or manage. Competitor analytics are NOT accessible via any official API.

Input: video ID(s), optional date range and metric list
Output: JSON with views, watch time, AVD, subs gained, etc. Exits 1 when any query failed.

Usage:
    python execution/fetch_video_analytics.py VIDEO_ID
    python execution/fetch_video_analytics.py VIDEO_ID --days 90
    python execution/fetch_video_analytics.py VIDEO_ID1 VIDEO_ID2 --metrics views,estimatedMinutesWatched
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.youtube_auth import TOKEN_PATH, get_oauth_service

# Thumbnail impressions and their CTR are not reports.query metrics; they come from the Reporting API's
# channel_reach_basic_a1 report (references/analytics-guide.md), so they are not requested here.
DEFAULT_METRICS = [
    "views",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "subscribersGained",
    "subscribersLost",
    "likes",
    "shares",
    "comments",
]

TRAFFIC_SOURCE_METRICS = [
    "views",
    "estimatedMinutesWatched",
]


def fetch_video_metrics(service, channel_id, video_ids, start_date, end_date, metrics):
    """Fetch standard metrics for specified videos."""
    filters = f"video=={','.join(video_ids)}"

    try:
        response = service.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date,
            endDate=end_date,
            metrics=",".join(metrics),
            filters=filters,
            dimensions="video",
            maxResults=200,
        ).execute()
    except Exception as e:
        return {"error": str(e)}

    rows = response.get("rows", [])
    headers = [h["name"] for h in response.get("columnHeaders", [])]
    results = []

    for row in rows:
        entry = dict(zip(headers, row))
        results.append(entry)

    return results


def fetch_traffic_sources(service, channel_id, video_ids, start_date, end_date):
    """Fetch traffic source breakdown for videos."""
    filters = f"video=={','.join(video_ids)}"

    try:
        response = service.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date,
            endDate=end_date,
            metrics=",".join(TRAFFIC_SOURCE_METRICS),
            filters=filters,
            dimensions="insightTrafficSourceType",
            maxResults=200,
        ).execute()
    except Exception as e:
        return {"error": str(e)}

    rows = response.get("rows", [])
    headers = [h["name"] for h in response.get("columnHeaders", [])]
    return [dict(zip(headers, row)) for row in rows]


def fetch_daily_metrics(service, channel_id, video_ids, start_date, end_date):
    """Fetch daily metric breakdown for trend analysis."""
    filters = f"video=={','.join(video_ids)}"
    daily_metrics = ["views", "estimatedMinutesWatched", "likes", "subscribersGained"]

    try:
        response = service.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date,
            endDate=end_date,
            metrics=",".join(daily_metrics),
            filters=filters,
            dimensions="day",
            sort="day",
            maxResults=200,
        ).execute()
    except Exception as e:
        return {"error": str(e)}

    rows = response.get("rows", [])
    headers = [h["name"] for h in response.get("columnHeaders", [])]
    return [dict(zip(headers, row)) for row in rows]


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube video analytics")
    parser.add_argument("video_ids", nargs="+", help="One or more video IDs")
    parser.add_argument("--days", type=int, default=28,
                        help="Number of days to look back (default: 28)")
    parser.add_argument("--metrics", type=str, default=None,
                        help="Comma-separated metrics (default: standard set)")
    parser.add_argument("--traffic-sources", action="store_true",
                        help="Include traffic source breakdown")
    parser.add_argument("--daily", action="store_true",
                        help="Include daily metric breakdown")

    args = parser.parse_args()

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    metrics = args.metrics.split(",") if args.metrics else DEFAULT_METRICS

    # Build OAuth service
    service, error = get_oauth_service()
    if error:
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

    # We need the YouTube Data API service to get channel ID
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
            yt = build("youtube", "v3", credentials=creds)
            ch_resp = yt.channels().list(part="id", mine=True).execute()
            channel_id = ch_resp["items"][0]["id"]
        else:
            print(json.dumps({"error": "OAuth token not found. Run auth first."}),
                  file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Failed to get channel ID: {e}"}),
              file=sys.stderr)
        sys.exit(1)

    # Fetch metrics
    result = {
        "video_ids": args.video_ids,
        "date_range": {"start": start_date, "end": end_date},
        "metrics": {},
        "fetched_at": datetime.now().isoformat(),
    }

    video_metrics = fetch_video_metrics(
        service, channel_id, args.video_ids, start_date, end_date, metrics
    )
    result["metrics"]["standard"] = video_metrics

    if args.traffic_sources:
        traffic = fetch_traffic_sources(
            service, channel_id, args.video_ids, start_date, end_date
        )
        result["metrics"]["traffic_sources"] = traffic

    if args.daily:
        daily = fetch_daily_metrics(
            service, channel_id, args.video_ids, start_date, end_date
        )
        result["metrics"]["daily"] = daily

    print(json.dumps(result, indent=2))
    if any(isinstance(v, dict) and "error" in v for v in result["metrics"].values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
