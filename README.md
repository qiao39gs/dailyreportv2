# 微信群聊日报生成器

读取微信聊天记录导出文件（TraceMemo 格式），调用 AI 生成结构化日报数据，渲染为 HTML 并截图导出 PNG 日报。

## 工作流程

```
聊天档案 (messages.js)  →  数据统计  →  AI 生成日报 JSON  →  Jinja2 渲染 HTML  →  Playwright 截图 PNG
```

1. **`chatlog.py`** — 从导出档案中按日期和群名筛选聊天记录，统计话唠榜、熬夜冠军、活跃时段等信息，并加载群成员头像（Base64 内联）。
2. **`report.py`** — 组装提示词（含统计结果 + 聊天记录 + 可视化 prompt），调用 OpenAI 兼容接口生成符合 JSON Schema 的日报数据，注入头像后渲染 HTML，最后用 Playwright 全页截图导出 PNG。
3. **`report_schema.py`** — 定义 AI 输出的 JSON Schema（热点话题、分享资源、重要消息、有趣对话、问答、数据面板、词云等）。
4. **`report_template.html` + `report.css`** — 日报页面模板与样式。
5. **`聊天记录可视化prompt.md`** — 指导 AI 生成日报内容的提示词，可自行调整。

## 目录结构

```
dailyreportv2/
├── main.py                       # 入口，逐个群组处理
├── config.py                     # 读取 .env 配置
├── chatlog.py                    # 聊天记录读取与统计分析
├── report.py                     # AI 调用、HTML 渲染、截图
├── report_schema.py              # AI 输出 JSON Schema
├── report_template.html          # 日报页面模板
├── report.css                    # 日报样式
├── 聊天记录可视化prompt.md         # AI 提示词
├── .env.example                  # 配置模板
└── output/                       # 输出目录（按 MMDD 分文件夹）
```

## 环境要求

- Python 3.10+
- 依赖：`openai`、`jinja2`、`playwright`、`python-dotenv`

```bash
pip install openai jinja2 playwright python-dotenv
playwright install chromium
```

## 配置

复制 `.env.example` 为 `.env` 并填写：

```ini
GROUP_LIST=群名1,群名2
BASE_URL=https://api.example.com/v1
API_KEY=your-api-key
MODEL=your-model
CHATLOG_EXPORT_ROOT=C:\Users\Administrator\Documents\TraceMemo\导出
OUTPUT_ROOT=C:\dev\dailyreportv2\output
```

| 变量 | 说明 |
| --- | --- |
| `GROUP_LIST` | 要生成日报的群名，逗号分隔 |
| `BASE_URL` | OpenAI 兼容接口地址 |
| `API_KEY` | 接口密钥 |
| `MODEL` | 模型名称 |
| `CHATLOG_EXPORT_ROOT` | 聊天档案导出根目录，其下需存在 `<群名>_聊天档案/data/messages.js` |
| `OUTPUT_ROOT` | 日报输出根目录 |

## 使用

```bash
python main.py
```

默认生成**前一天**的日报；也可在代码中调用指定日期：

```python
from main import main
main("2026-09-27")
```

产物输出到 `OUTPUT_ROOT/<MMDD>/`：

- `prompt_<群名>.md` — 完整提示词（便于调试）
- `index_<群名>.html` — 日报网页
- `index_<群名>.png` — 日报长图（宽度 1800px）

## 自定义

- **调整日报名内容/风格**：编辑 `聊天记录可视化prompt.md`
- **调整输出字段**：编辑 `report_schema.py` 并在 `report_template.html` 中同步渲染
- **调整排版样式**：编辑 `report.css`
