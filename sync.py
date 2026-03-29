import os
import httpx
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
POLICE_API_URL = "https://polisen.se/api/events"


def fetch_events() -> list[dict]:
    response = httpx.get(POLICE_API_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def transform_event(event: dict) -> dict:
    location = event.get("location", {})
    return {
        "id": event["id"],
        "datetime": event["datetime"],
        "name": event["name"],
        "summary": event.get("summary"),
        "url": event.get("url"),
        "type": event.get("type"),
        "location_name": location.get("name"),
        "location_gps": location.get("gps"),
    }


def sync():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("Fetching events from polisen.se...")
    events = fetch_events()
    print(f"Fetched {len(events)} events")

    rows = [transform_event(e) for e in events]

    print("Upserting into Supabase...")
    result = supabase.table("police_events").upsert(rows, on_conflict="id").execute()
    print(f"Done. {len(result.data)} rows upserted.")


if __name__ == "__main__":
    sync()
