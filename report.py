import os
import json
from datetime import datetime
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
from config import BASE_URL, API_KEY, MODEL, PROMPT_PATH, OUTPUT_ROOT
from chatlog import filter_media
from report_schema import REPORT_JSON_SCHEMA

def build_prompt(analyze_dict, chatlog_content, prompt_md):
    top_users = "".join(f"   {i+1}. {u}: {c}条\n"
                        for i, (u, c) in enumerate(analyze_dict['top_10_users']))
    night = (f"   - {analyze_dict['night_owl_king']} : {analyze_dict['night_owl_count']} 条消息\n"
             if analyze_dict['night_owl_king'] else "")
    return (
        f"以下信息使用真实数据：\n话唠榜：\n{top_users}熬夜冠军 (23:00 - 06:59)：\n{night}"
        f"\n---\n【聊天记录】\n{filter_media(chatlog_content)}"
        f"\n---\n【可视化prompt】\n{prompt_md}"
        f"\n---\n请分析微信群聊天记录，生成日报数据。"
    )

def call_ai(analyze_dict, chatlog_content, date, avatar_data=None):
    with open(PROMPT_PATH, encoding="utf-8") as f:
        prompt_md = f.read()
    prompt = build_prompt(analyze_dict, chatlog_content, prompt_md)

    mmdd = datetime.strptime(date, "%Y-%m-%d").strftime("%m%d")
    target_dir = os.path.join(OUTPUT_ROOT, mmdd)
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, f"prompt_{analyze_dict['group_name']}.md"), "w", encoding="utf-8") as f:
        f.write(prompt)
    print("完整提示词已生成并保存，正在生成报告JSON数据...")

    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format=REPORT_JSON_SCHEMA
    )
    report_data = json.loads(response.choices[0].message.content)
    for w in report_data.get('wordCloud', []):
        if isinstance(w.get('size'), str):
            w['size'] = w['size'].rstrip('px')
    topic_heatmap = report_data.get('analytics', {}).get('topicHeatmap', [])
    percentages = [item.get('percentage') for item in topic_heatmap]
    if percentages and all(isinstance(value, (int, float)) for value in percentages):
        if max(percentages) <= 1 and abs(sum(percentages) - 1) <= 0.01:
            for item in topic_heatmap:
                percentage = float(round(item['percentage'] * 100, 2))
                item['percentage'] = int(percentage) if percentage.is_integer() else percentage
    avatar_data = avatar_data or {}
    for resource in report_data.get('sharedResources', []):
        resource['avatar'] = avatar_data.get(resource.get('sharedBy'))
    for message in report_data.get('importantMessages', []):
        message['avatar'] = avatar_data.get(message.get('sender'))
    for dialogue in report_data.get('interestingDialogues', []):
        for message in dialogue.get('content', []):
            message['avatar'] = avatar_data.get(message.get('speaker'))
    for qa in report_data.get('questionsAnswers', []):
        question = qa.get('question', {})
        question['avatar'] = avatar_data.get(question.get('asker'))
        for answer in qa.get('answers', []):
            answer['avatar'] = avatar_data.get(answer.get('responder'))
    analytics = report_data.get('analytics', {})
    for participant in analytics.get('chatterboard', []):
        participant['avatar'] = avatar_data.get(participant.get('name'))
    night_owl = analytics.get('nightOwl', {})
    night_owl['avatar'] = avatar_data.get(night_owl.get('name'))
    report_data['reportInfo'] = {
        "groupName": analyze_dict['group_name'],
        "date": date,
        "generationTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messageCount": analyze_dict['total_messages'],
        "activeUsers": analyze_dict['total_speakers'],
        "timeRange": f"{analyze_dict['min_time'][:5]} - {analyze_dict['max_time'][:5]}"
    }
    return report_data

def render_html(report_data, analyze_dict, date):
    css_path = os.path.join(os.path.dirname(__file__), "report.css")
    with open(css_path, encoding="utf-8") as f:
        inline_css = f.read()
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    html = env.get_template('report_template.html').render(**report_data, inline_css=inline_css)

    mmdd = datetime.strptime(date, "%Y-%m-%d").strftime("%m%d")
    target_dir = os.path.join(OUTPUT_ROOT, mmdd)
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, f"index_{analyze_dict['group_name']}.html")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML已保存到: {target_file}")
    return target_file, target_dir

def screenshot_html(target_file, target_dir, group_name):
    img_name = f"index_{group_name}.png"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 800, "height": 5000})
        page.goto(f"file:///{target_file.replace(os.sep, '/')}")
        page.screenshot(path=os.path.join(target_dir, img_name), full_page=True)
        browser.close()
    print(f"图片已保存到: {os.path.join(target_dir, img_name)}")
