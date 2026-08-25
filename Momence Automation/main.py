import os
from datetime import datetime, timedelta, timezone
import requests
from dotenv import load_dotenv
from google import genai
from config import ROOM_OVERHEAD_PER_HOUR, INSTRUCTOR_RATES

load_dotenv()

MOMENCE_BASE_URL = "https://api.momence.com/api/v2"
CLIENT_ID = os.getenv("MOMENCE_CLIENT_ID", "your_client_id_here")
CLIENT_SECRET = os.getenv("MOMENCE_CLIENT_SECRET", "your_client_secret_here")
SERVICE_EMAIL = os.getenv("MOMENCE_SERVICE_EMAIL", "your_email_here")
SERVICE_PASSWORD = os.getenv("MOMENCE_SERVICE_PASSWORD", "your_password_here")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


class MomenceClient:
    """Production Momence API v2 Client with built-in sandbox fallback."""

    def __init__(self):
        self.sandbox_mode = CLIENT_ID == "your_client_id_here"
        if not self.sandbox_mode:
            self.access_token = self._authenticate()
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
            }
        else:
            print("[INFO] No live API keys found in .env. Running in Momence V2 Sandbox Mode.\n")
            self.headers = {}

    def _authenticate(self) -> str:
        token_url = f"{MOMENCE_BASE_URL}/auth/token"
        payload = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": SERVICE_EMAIL,
            "password": SERVICE_PASSWORD,
        }
        res = requests.post(token_url, json=payload)
        res.raise_for_status()
        return res.json()["access_token"]

    def get_sessions(self, start_date: datetime, end_date: datetime) -> list:
        """Fetches host class sessions from Momence V2 /member/host/sessions."""
        if self.sandbox_mode:
            now = datetime.now(timezone.utc)
            return [
                {
                    "id": 101,
                    "name": "Reformer Pilates - Beginner",
                    "startsAt": (now + timedelta(hours=24)).isoformat(),
                    "capacity": 12,
                    "participants": 0,
                    "isCancelled": False,
                    "teacher": {"firstName": "Sarah", "lastName": "Jenkins"},
                    "fixedTicketPrice": 35.0,
                    "attendees": [],
                },
                {
                    "id": 102,
                    "name": "Mat Pilates - Morning Flow",
                    "startsAt": (now - timedelta(days=21)).isoformat(),
                    "capacity": 20,
                    "participants": 4,
                    "isCancelled": False,
                    "teacher": {"firstName": "Alex", "lastName": "Rivera"},
                    "fixedTicketPrice": 25.0,
                    "attendees": [{"id": 1, "name": "Jessica Taylor"}, {"id": 2, "name": "Mark Miller"}],
                },
                {
                    "id": 103,
                    "name": "Mat Pilates - Morning Flow",
                    "startsAt": (now - timedelta(days=14)).isoformat(),
                    "capacity": 20,
                    "participants": 5,
                    "isCancelled": False,
                    "teacher": {"firstName": "Alex", "lastName": "Rivera"},
                    "fixedTicketPrice": 25.0,
                    "attendees": [{"id": 1, "name": "Jessica Taylor"}, {"id": 3, "name": "Emma Watson"}],
                },
                {
                    "id": 104,
                    "name": "Mat Pilates - Morning Flow",
                    "startsAt": (now - timedelta(days=7)).isoformat(),
                    "capacity": 20,
                    "participants": 3,
                    "isCancelled": False,
                    "teacher": {"firstName": "Alex", "lastName": "Rivera"},
                    "fixedTicketPrice": 25.0,
                    "attendees": [{"id": 1, "name": "Jessica Taylor"}],
                },
                {
                    "id": 105,
                    "name": "Power Reformer",
                    "startsAt": (now - timedelta(days=14)).isoformat(),
                    "capacity": 10,
                    "participants": 9,
                    "isCancelled": False,
                    "teacher": {"firstName": "Sarah", "lastName": "Jenkins"},
                    "fixedTicketPrice": 40.0,
                    "attendees": [{"id": 1, "name": "Jessica Taylor"}],
                },
            ]

        sessions_url = f"{MOMENCE_BASE_URL}/member/host/sessions"
        params = {"from": start_date.isoformat(), "to": end_date.isoformat()}
        res = requests.get(sessions_url, headers=self.headers, params=params)
        res.raise_for_status()
        return res.json() if isinstance(res.json(), list) else res.json().get("sessions", [])

    def get_members(self) -> list:
        """Fetches host member records from Momence V2 /host/members."""
        if self.sandbox_mode:
            return [
                {"id": 1, "name": "Jessica Taylor", "membership_type": "drop_in", "status": "active", "visits_last_14d": 6},
                {"id": 2, "name": "Mark Miller", "membership_type": "unlimited_monthly", "status": "active", "visits_last_14d": 2},
                {"id": 3, "name": "Emma Watson", "membership_type": "10_class_pack", "status": "active", "visits_last_14d": 4},
                {"id": 4, "name": "David Smith", "membership_type": "unlimited_monthly", "status": "canceled", "visits_last_14d": 0},
                {"id": 5, "name": "Chloe Bennett", "membership_type": "unlimited_monthly", "status": "canceled", "visits_last_14d": 0},
            ]

        members_url = f"{MOMENCE_BASE_URL}/host/members"
        res = requests.get(members_url, headers=self.headers)
        res.raise_for_status()
        return res.json() if isinstance(res.json(), list) else res.json().get("members", [])


# -------------------------------------------------------------------------
# Rule Implementations
# -------------------------------------------------------------------------

def check_48h_empty_classes(client: MomenceClient) -> list:
    """Rule 1: 48 hours notice where no one is booked into a class."""
    now = datetime.now(timezone.utc)
    in_48_hours = now + timedelta(hours=48)

    sessions = client.get_sessions(start_date=now, end_date=in_48_hours)
    empty_classes = []

    for session in sessions:
        is_cancelled = session.get("isCancelled", False)
        participants_count = session.get("participants", 0)

        if not is_cancelled and participants_count == 0:
            teacher_info = session.get("teacher") or {}
            teacher_name = f"{teacher_info.get('firstName', '')} {teacher_info.get('lastName', '')}".strip() or "Unassigned"
            empty_classes.append({
                "session_id": session.get("id"),
                "name": session.get("name"),
                "starts_at": session.get("startsAt"),
                "capacity": session.get("capacity"),
                "instructor": teacher_name,
            })

    return empty_classes


def check_3week_capacity_trends(client: MomenceClient) -> dict:
    """Rules 2 & 3: Classes below 50% or above 80% capacity over last 3 weeks."""
    now = datetime.now(timezone.utc)
    three_weeks_ago = now - timedelta(days=21)

    sessions = client.get_sessions(start_date=three_weeks_ago, end_date=now)
    slot_stats = {}

    for session in sessions:
        name = session.get("name")
        capacity = session.get("capacity", 1)
        participants = session.get("participants", 0)

        utilization = participants / capacity if capacity > 0 else 0

        if name not in slot_stats:
            slot_stats[name] = {"total_utilization": 0.0, "count": 0}

        slot_stats[name]["total_utilization"] += utilization
        slot_stats[name]["count"] += 1

    underutilized = []
    overutilized = []

    for class_name, stats in slot_stats.items():
        avg_capacity = stats["total_utilization"] / stats["count"]
        if avg_capacity < 0.50:
            underutilized.append({"class_name": class_name, "avg_capacity_pct": round(avg_capacity * 100, 1)})
        elif avg_capacity > 0.80:
            overutilized.append({"class_name": class_name, "avg_capacity_pct": round(avg_capacity * 100, 1)})

    return {"underutilized": underutilized, "overutilized": overutilized}


def check_unprofitable_classes(client: MomenceClient) -> list:
    """Rule 4: Identifies class slots with negative net profit over the last 3 weeks."""
    now = datetime.now(timezone.utc)
    three_weeks_ago = now - timedelta(days=21)

    sessions = client.get_sessions(start_date=three_weeks_ago, end_date=now)
    slot_financials = {}

    for session in sessions:
        name = session.get("name")
        participants = session.get("participants", 0)
        ticket_price = session.get("fixedTicketPrice", 0.0)

        teacher_info = session.get("teacher") or {}
        teacher_name = f"{teacher_info.get('firstName', '')} {teacher_info.get('lastName', '')}".strip() or "Default"

        session_revenue = participants * ticket_price
        instructor_pay = INSTRUCTOR_RATES.get(teacher_name, INSTRUCTOR_RATES.get("Default", 25.00))
        total_cost = instructor_pay + ROOM_OVERHEAD_PER_HOUR
        net_profit = session_revenue - total_cost

        if name not in slot_financials:
            slot_financials[name] = {"total_profit": 0.0, "total_revenue": 0.0, "sessions_count": 0}

        slot_financials[name]["total_profit"] += net_profit
        slot_financials[name]["total_revenue"] += session_revenue
        slot_financials[name]["sessions_count"] += 1

    unprofitable = []
    for class_name, fin in slot_financials.items():
        if fin["total_profit"] < 0:
            unprofitable.append({
                "class_name": class_name,
                "total_loss": round(fin["total_profit"], 2),
                "total_revenue": round(fin["total_revenue"], 2),
                "sessions_run": fin["sessions_count"]
            })

    return unprofitable


def check_business_kpis_and_rankings(client: MomenceClient) -> dict:
    """Rules 5 & 6: Overall Business KPIs and Top/Bottom Class Rankings."""
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    sessions = client.get_sessions(start_date=thirty_days_ago, end_date=now)

    total_revenue = 0.0
    total_profit = 0.0
    total_capacity = 0
    total_participants = 0
    class_metrics = {}

    for session in sessions:
        name = session.get("name")
        capacity = session.get("capacity", 1)
        participants = session.get("participants", 0)
        ticket_price = session.get("fixedTicketPrice", 0.0)

        teacher_info = session.get("teacher") or {}
        teacher_name = f"{teacher_info.get('firstName', '')} {teacher_info.get('lastName', '')}".strip() or "Default"

        revenue = participants * ticket_price
        instructor_pay = INSTRUCTOR_RATES.get(teacher_name, INSTRUCTOR_RATES.get("Default", 25.00))
        cost = instructor_pay + ROOM_OVERHEAD_PER_HOUR
        net_profit = revenue - cost

        total_revenue += revenue
        total_profit += net_profit
        total_capacity += capacity
        total_participants += participants

        if name not in class_metrics:
            class_metrics[name] = {
                "total_revenue": 0.0,
                "total_profit": 0.0,
                "total_capacity": 0,
                "total_participants": 0,
            }

        class_metrics[name]["total_revenue"] += revenue
        class_metrics[name]["total_profit"] += net_profit
        class_metrics[name]["total_capacity"] += capacity
        class_metrics[name]["total_participants"] += participants

    rankings = []
    for class_name, metrics in class_metrics.items():
        cap_pct = (metrics["total_participants"] / metrics["total_capacity"] * 100) if metrics["total_capacity"] > 0 else 0
        profit_margin = (metrics["total_profit"] / metrics["total_revenue"] * 100) if metrics["total_revenue"] > 0 else -100.0

        rankings.append({
            "class_name": class_name,
            "net_profit": round(metrics["total_profit"], 2),
            "profit_margin_pct": round(profit_margin, 1),
            "capacity_pct": round(cap_pct, 1)
        })

    by_profit = sorted(rankings, key=lambda x: x["net_profit"], reverse=True)
    by_capacity = sorted(rankings, key=lambda x: x["capacity_pct"], reverse=True)

    overall_capacity = (total_participants / total_capacity * 100) if total_capacity > 0 else 0

    return {
        "kpis": {
            "total_revenue": round(total_revenue, 2),
            "total_net_profit": round(total_profit, 2),
            "overall_capacity_pct": round(overall_capacity, 1),
        },
        "top_by_profit": by_profit[:2],
        "lowest_by_profit": by_profit[-2:],
        "top_by_capacity": by_capacity[:2],
        "lowest_by_capacity": by_capacity[-2:],
    }


def check_membership_health_and_upsells(client: MomenceClient) -> dict:
    """Rules 8 & 9: Membership Churn/Retention and Non-Member Upsell Targets."""
    members = client.get_members()
    total_members = len(members)

    if total_members == 0:
        return {"churn_rate_pct": 0.0, "retention_rate_pct": 100.0, "upsell_candidates": []}

    active_members = [m for m in members if m.get("status") == "active"]
    canceled_members = [m for m in members if m.get("status") == "canceled"]

    churn_rate = (len(canceled_members) / total_members) * 100
    retention_rate = (len(active_members) / total_members) * 100

    upsell_candidates = []
    for member in active_members:
        is_non_recurring = member.get("membership_type") in ["drop_in", "10_class_pack", None]
        high_attendance = member.get("visits_last_14d", 0) >= 6

        if is_non_recurring and high_attendance:
            upsell_candidates.append({
                "member_name": member.get("name"),
                "current_pass": member.get("membership_type"),
                "visits_last_14d": member.get("visits_last_14d"),
                "recommendation": "Pitch Unlimited Monthly Membership (attending ~3x/week)"
            })

    return {
        "churn_rate_pct": round(churn_rate, 1),
        "retention_rate_pct": round(retention_rate, 1),
        "active_members_count": len(active_members),
        "upsell_candidates": upsell_candidates
    }


def generate_ai_schedule_recommendations(capacity_alerts: dict, unprofitable_alerts: list) -> str:
    """Rule 7: Recommendations for schedule changes using Gemini AI."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return "[INFO] GEMINI_API_KEY missing in .env. Add your key to generate live AI schedule recommendations."

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    You are an expert Pilates Studio Operations Consultant.
    Review the following studio session performance data over the last 3 weeks and provide 3 concrete, realistic schedule adjustments.

    DATA SUMMARY:
    - Underutilized Classes (<50% Capacity): {capacity_alerts['underutilized']}
    - Overutilized Classes (>80% Capacity): {capacity_alerts['overutilized']}
    - Unprofitable Class Slots (Negative Net Revenue): {unprofitable_alerts}

    Provide recommendations in bullet points covering:
    1. Which underperforming or unprofitable classes to swap, cancel, or re-level.
    2. Which high-demand class types or times to expand.
    3. The specific business rationale based on capacity and revenue data.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text


def send_slack_digest(empty_alerts, capacity_alerts, unprofitable_alerts, membership_report, ai_recommendations):
    """Dispatches a structured, visually polished executive report to Slack."""
    slack_url = os.getenv("SLACK_WEBHOOK_URL")
    if not slack_url or slack_url == "your_slack_webhook_here":
        print("\n[INFO] SLACK_WEBHOOK_URL missing in .env. Skipping Slack dispatch.")
        return

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "📊 Studio Executive Operations Digest", "emoji": True}
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"🟢 *Retention Rate*\n`{membership_report['retention_rate_pct']}%`"},
                {"type": "mrkdwn", "text": f"🔴 *Churn Rate*\n`{membership_report['churn_rate_pct']}%`"},
                {"type": "mrkdwn", "text": f"⚠️ *48h Empty Classes*\n`{len(empty_alerts)} session(s)`"},
                {"type": "mrkdwn", "text": f"💸 *Unprofitable Slots*\n`{len(unprofitable_alerts)} slot(s)`"}
            ]
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🎯 *Membership Upsell Opportunities*\n" + (
                    "\n".join([f"• *{u['member_name']}* (`{u['current_pass']}`) → *{u['visits_last_14d']} visits in 14 days* (Recommend Unlimited Pass)" for u in membership_report['upsell_candidates']])
                    if membership_report['upsell_candidates'] else "_No non-recurring members qualified today._"
                )
            }
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"💡 *AI Schedule Recommendations*\n{ai_recommendations}"
            }
        }
    ]

    payload = {"blocks": blocks}
    res = requests.post(slack_url, json=payload)
    if res.status_code == 200:
        print("\n[SUCCESS] Formatted executive digest posted to Slack!")
    else:
        print(f"\n[ERROR] Slack dispatch failed: {res.status_code} - {res.text}")


# -------------------------------------------------------------------------
# Execution Pipeline
# -------------------------------------------------------------------------

if __name__ == "__main__":
    client = MomenceClient()

    # Rule 1
    empty_alerts = check_48h_empty_classes(client)
    print(f"--- Rule 1: 48-Hour Empty Class Alerts ({len(empty_alerts)} Found) ---")
    for alert in empty_alerts:
        print(f"ID: {alert['session_id']} | Class: {alert['name']} | Starts: {alert['starts_at']} | Instructor: {alert['instructor']}")

    print("\n" + "=" * 60 + "\n")

    # Rules 2 & 3
    capacity_alerts = check_3week_capacity_trends(client)
    print("--- Rules 2 & 3: 3-Week Capacity Trends ---")
    print("Underutilized (<50% Capacity):", capacity_alerts["underutilized"])
    print("Overutilized (>80% Capacity):", capacity_alerts["overutilized"])

    print("\n" + "=" * 60 + "\n")

    # Rule 4
    unprofitable_alerts = check_unprofitable_classes(client)
    print("--- Rule 4: 3-Week Unprofitable Class Slots ---")
    print(unprofitable_alerts)

    print("\n" + "=" * 60 + "\n")

    # Rules 5 & 6
    kpi_report = check_business_kpis_and_rankings(client)
    print("--- Rules 5 & 6: Business KPIs & Rankings ---")
    print("KPIs:", kpi_report["kpis"])
    print("Top by Profit:", kpi_report["top_by_profit"])
    print("Lowest by Profit:", kpi_report["lowest_by_profit"])

    print("\n" + "=" * 60 + "\n")

    # Rules 8 & 9
    membership_report = check_membership_health_and_upsells(client)
    print("--- Rules 8 & 9: Membership Health & Upsell Candidates ---")
    print(f"Active Members: {membership_report['active_members_count']} | Retention: {membership_report['retention_rate_pct']}% | Churn: {membership_report['churn_rate_pct']}%")
    print("Upsell Candidates:", membership_report["upsell_candidates"])

    print("\n" + "=" * 60 + "\n")

    # Rule 7
    print("--- Rule 7: AI Schedule Change Recommendations (Gemini) ---")
    ai_recommendations = generate_ai_schedule_recommendations(capacity_alerts, unprofitable_alerts)
    print(ai_recommendations)

    # Slack Dispatch
    send_slack_digest(empty_alerts, capacity_alerts, unprofitable_alerts, membership_report, ai_recommendations)