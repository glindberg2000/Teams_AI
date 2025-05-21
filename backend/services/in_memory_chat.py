from datetime import datetime

# In-memory message store: { (team_id, channel): [msg, ...] }
in_memory_messages = {}


def store_message(team_id, user, message, channel="general"):
    key = (team_id, channel)
    if key not in in_memory_messages:
        in_memory_messages[key] = []
    msg = {
        "id": len(in_memory_messages[key]) + 1,
        "team_id": team_id,
        "user": user,
        "message": message,
        "channel": channel,
        "timestamp": datetime.utcnow().isoformat(),
    }
    in_memory_messages[key].append(msg)
    return msg
