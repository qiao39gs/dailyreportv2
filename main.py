from datetime import datetime, timedelta
from chatlog import fetch_chat_log, analyze_chat, load_avatar_data
from report import call_ai, render_html, screenshot_html
from config import GROUP_LIST

def main(date=None):
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    for group in GROUP_LIST:
        print(f"\n=== 处理群组：{group} ===")
        chatlog = fetch_chat_log(date, group)
        analyze_dict = analyze_chat(chatlog, group)
        avatar_data = load_avatar_data(group)
        report_data = call_ai(analyze_dict, chatlog, date, avatar_data)
        target_file, target_dir = render_html(report_data, analyze_dict, date)
        screenshot_html(target_file, target_dir, analyze_dict['group_name'])

if __name__ == "__main__":
    main()
