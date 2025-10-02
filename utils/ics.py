from datetime import datetime
import pandas as pd

def _dtfmt(ts: str) -> str:
    # Espera formato ISO-like "YYYY-MM-DD HH:MM"
    try:
        dt = pd.to_datetime(ts)
    except Exception:
        dt = datetime.utcnow()
    return dt.strftime("%Y%m%dT%H%M%S")

def build_ics(sessions_df: pd.DataFrame, calendar_name: str = "Mi Feria"):
    lines = []
    lines.append("BEGIN:VCALENDAR")
    lines.append("VERSION:2.0")
    lines.append(f"X-WR-CALNAME:{calendar_name}")
    for _, row in sessions_df.iterrows():
        uid = f"{row['sub_id']}@feria"
        dtstart = _dtfmt(str(row['start']))
        dtend = _dtfmt(str(row['end']))
        # Usar project_title si existe, si no usar title
        title = str(row.get('project_title', row.get('title', ''))).replace("\\n"," ")
        desc = f"Track: {row.get('track','-')}"
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART:{dtstart}",
            f"DTEND:{dtend}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{desc}",
            "END:VEVENT"
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)
