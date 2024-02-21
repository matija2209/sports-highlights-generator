timestamps = [
    "5:18 — Tekma I",
    "10:12 — PRILOŽNOST",
    "12:55 — GOL",
    "14:20 — Tekma II",
    "22:45 — Tekma III",
    "26:21 — PRILOŽNOST",
    "27:45 — GOL",
    "29:48 — GOL (Mark)",
    "31:20 — Tekma IV",
    "37:45 — GOL (Tim)",
    "38:45 — GOL (Aleks...)",
    "39:10 — PRILOŽNOST",
    "39:15 — PRILOŽNOST",
    "40:14 — Tekma V",
    "41:43 — Izbijanje NM",
    "46:20 — GREAT GOL",
    "48:50 — Tekma VI",
    "51:43 — GOL",
    "55:10 — POŠKODBA",
    "56:38 — GOL",
    "57:39 — Tekma VII",
    "59:05 — GOL (Filip)",
    "1:02:03 — PRILOŽNOST",
    "1:02:15 — GOL",
    "1:04:41 — GOL",
    "1:06:46 — Tekma VIII",
    "1:13:29 — Piša Matic",
    "1:15:28 — GOL",
    "1:16:10 — Tekma IX",
    "1:17:48 — PODAJA",
    "1:18:10 — \"Faul\" nad Žetkotom",
    "1:20:28 - PODAJA",
    "1:20:55 — GOL",
    "1:22:08 — GOL",
    "1:24:15 — GOL",
    "1:27:30 — Tekma X",
    "1:36:52 — Piša Žan"
]

def convert_to_seconds(timestamp):
    parts = timestamp.split(':')
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    else:
        return 0

def process_timestamps_corrected(timestamps):
    results = []
    for timestamp in timestamps:
        # Splitting the string into time and description parts
        parts = timestamp.split(' — ')
        if len(parts) == 2:
            time, description = parts
            time_in_seconds = convert_to_seconds(time)

            # Further split the description to separate the event type and associated name (if any)
            event_parts = description.split(' (')
            event_type = event_parts[0]
            event_name = event_parts[1][:-1] if len(event_parts) > 1 else ""

            results.append({"timestamp": time_in_seconds, "type": event_type, "name": event_name})
    return results

processed_timestamps = process_timestamps(timestamps)