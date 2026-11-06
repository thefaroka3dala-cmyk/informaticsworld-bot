import datetime, os, sys

OFFSET = 3  # UTC+3 (Saudi / Iraq time)


def check(file, gap_hours, start_hour, end_hour):
    """Exit quietly unless it is time to post. Manual runs always pass."""
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        return
    now = datetime.datetime.now(datetime.timezone.utc)
    hour = (now + datetime.timedelta(hours=OFFSET)).hour
    if not (start_hour <= hour <= end_hour):
        print("outside posting hours, skipping")
        sys.exit(0)
    try:
        last = datetime.datetime.fromisoformat(open(file).read().strip())
    except Exception:
        last = None
    if last and (now - last).total_seconds() < gap_hours * 3600:
        print("too soon since last post, skipping")
        sys.exit(0)


def mark(file):
    now = datetime.datetime.now(datetime.timezone.utc)
    open(file, "w").write(now.isoformat())
