import base64
import json
import mimetypes
import re
from datetime import datetime
from pathlib import Path
from collections import Counter
from config import CHATLOG_EXPORT_ROOT

def _load_export(group_name):
    archive_dir = (
        Path(CHATLOG_EXPORT_ROOT)
        / f"{group_name}_聊天档案"
    )
    messages_path = (
        archive_dir
        / "data"
        / "messages.js"
    )
    if not messages_path.is_file():
        raise FileNotFoundError(f"找不到聊天记录文件：{messages_path}")

    source = messages_path.read_text(encoding="utf-8-sig").strip()
    match = re.fullmatch(r"window\.__WECHAT_EXPORT__\s*=\s*(.*?);?", source, re.DOTALL)
    if not match:
        raise ValueError(f"无法识别 messages.js 格式：{messages_path}")

    return archive_dir, messages_path, json.loads(match.group(1))

def fetch_chat_log(date, group_name):
    _, messages_path, export_data = _load_export(group_name)
    target_date = datetime.strptime(date, "%Y-%m-%d").date()
    records = []
    for message in export_data.get("messages", []):
        if message.get("exportConversationName") != group_name:
            continue

        message_time = datetime.strptime(message["datetime"], "%Y/%m/%d %H:%M:%S")
        if message_time.date() != target_date:
            continue

        name = message.get("name", "").strip()
        sender_id = message.get("senderId", "").strip()
        if not name:
            continue

        content = message.get("content", "").strip()
        if not content:
            content = f"[{message.get('type', '未知消息')}]"
        records.append(
            f"{name}({sender_id}) {message_time:%H:%M:%S}\n{content}"
        )

    print(f"从聊天档案读取到 {len(records)} 条记录：{messages_path}")
    return "\n\n".join(records)

def load_avatar_data(group_name):
    archive_dir, _, export_data = _load_export(group_name)
    avatar_data = {}
    for message in export_data.get("messages", []):
        name = message.get("name", "").strip()
        avatar_url = message.get("exportAvatarUrl", "").strip()
        if not name or not avatar_url or name in avatar_data:
            continue

        avatar_path = archive_dir / avatar_url
        if not avatar_path.is_file():
            continue

        mime_type = mimetypes.guess_type(avatar_path.name)[0] or "image/jpeg"
        encoded = base64.b64encode(avatar_path.read_bytes()).decode("ascii")
        avatar_data[name] = f"data:{mime_type};base64,{encoded}"
    return avatar_data

def analyze_chat(chatlog_text, group_name):
    user_counts = Counter()
    night_owl_counts = Counter()
    times = []
    pattern = re.compile(r'\d{2}:\d{2}:\d{2}$')
    for line in chatlog_text.splitlines():
        line = line.strip()
        if not line or line[0] == ">":
            continue
        match = pattern.search(line)
        if not match:
            continue
        time_str = match.group(0)
        times.append(time_str)
        user_string = line[:match.start()].strip()
        last_paren = user_string.rfind('(')
        username = user_string[:last_paren].strip() if last_paren != -1 else user_string.split()[0] if user_string.split() else None
        if not username:
            continue
        user_counts[username] += 1
        if int(time_str[:2]) >= 23 or int(time_str[:2]) < 7:
            night_owl_counts[username] += 1
    night_owl = night_owl_counts.most_common(1)[0] if night_owl_counts else (None, 0)
    return {
        "group_name": group_name,
        "total_messages": sum(user_counts.values()),
        "total_speakers": len(user_counts),
        "top_10_users": user_counts.most_common(10),
        "night_owl_king": night_owl[0],
        "night_owl_count": night_owl[1],
        "min_time": min(times) if times else "00:00:00",
        "max_time": max(times) if times else "23:59:59",
    }

def filter_media(chatlog_text):
    skip = ('![图片]', '![动画表情]',
            'http://vweixinf.tc.qq.com',
            'http://wxapp.tc.qq.com',
            'http://localhost:5030',
            )
    lines = [
        "【img】" if any(s in l for s in skip) else l.strip()
        for l in chatlog_text.splitlines() if l.strip()
    ]
    return re.sub(r'\(wxid_[^)]*\)', '', '\n'.join(lines))
