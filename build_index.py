#!/usr/bin/env python3
"""
自动扫描当前目录下的所有 *.html 博客（除了 index.html 本身），
生成首页 index.html。

文件名规则：建议用 "序号-标识.html"（如 04-karpathy-makemore-ep3-batchnorm.html）
首页会按文件名排序展示。
"""
import os
import re
import datetime
from pathlib import Path

ROOT = Path(__file__).parent

# 站点元信息
SITE_TITLE = "dekiehu 的 AI 学习博客"
SITE_SUBTITLE = "Kafka 内核工程师转 AI Infra 的学习笔记"
SITE_DESC = "从 Karpathy Zero to Hero 开始，记录从神经网络基础到 LLM 推理引擎的完整学习路径。"


def extract_title(html_path: Path) -> str:
    """从 HTML 文件中提取 <title> 标签内容。"""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read(8000)  # 只读前 8KB 找 title 足够
        m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return html_path.stem


def extract_subtitle(html_path: Path) -> str:
    """从 HTML 文件中提取 .subtitle 内容（如果有）。"""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read(16000)
        m = re.search(
            r'<div\s+class="subtitle"[^>]*>(.*?)</div>',
            content,
            re.IGNORECASE | re.DOTALL,
        )
        if m:
            text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            return text[:200]
    except Exception:
        pass
    return ""


def extract_tags(html_path: Path) -> list:
    """从 HTML 文件中提取 .tag 标签列表。"""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read(16000)
        tags = re.findall(
            r'<span\s+class="tag"[^>]*>(.*?)</span>', content, re.IGNORECASE | re.DOTALL
        )
        return [re.sub(r"<[^>]+>", "", t).strip() for t in tags[:6]]
    except Exception:
        return []


def get_mtime(html_path: Path) -> str:
    ts = html_path.stat().st_mtime
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def collect_posts():
    posts = []
    for html in sorted(ROOT.glob("*.html")):
        if html.name == "index.html":
            continue
        posts.append(
            {
                "filename": html.name,
                "title": extract_title(html),
                "subtitle": extract_subtitle(html),
                "tags": extract_tags(html),
                "date": get_mtime(html),
            }
        )
    return posts


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{site_title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{site_desc}">
<style>
  :root {{
    --bg: #fbfaf7;
    --fg: #1f2328;
    --muted: #57606a;
    --accent: #0969da;
    --accent2: #8250df;
    --border: #d0d7de;
    --card-bg: #ffffff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
      "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--fg);
    line-height: 1.7;
    max-width: 920px;
    margin: 0 auto;
    padding: 56px 28px 96px;
    font-size: 16px;
  }}
  header {{
    border-bottom: 2px solid var(--border);
    padding-bottom: 24px;
    margin-bottom: 36px;
  }}
  h1 {{
    font-size: 34px;
    margin: 0 0 6px;
    line-height: 1.25;
  }}
  .site-subtitle {{
    color: var(--muted);
    font-size: 15px;
    margin: 0 0 14px;
  }}
  .site-desc {{
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
  }}
  .stats {{
    color: var(--muted);
    font-size: 13px;
    margin-top: 12px;
  }}

  .posts {{
    list-style: none;
    padding: 0;
    margin: 0;
  }}
  .post {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 22px 24px;
    margin-bottom: 18px;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  }}
  .post:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    border-color: var(--accent);
  }}
  .post a {{
    text-decoration: none;
    color: inherit;
    display: block;
  }}
  .post-title {{
    font-size: 19px;
    font-weight: 600;
    color: var(--accent);
    margin: 0 0 6px;
    line-height: 1.4;
  }}
  .post-subtitle {{
    color: var(--muted);
    font-size: 14px;
    margin: 0 0 12px;
    line-height: 1.55;
  }}
  .post-meta {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    font-size: 12.5px;
  }}
  .post-date {{
    color: var(--muted);
  }}
  .tag {{
    display: inline-block;
    background: #f6f8fa;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1px 10px;
    font-size: 12px;
    color: var(--muted);
  }}

  footer {{
    margin-top: 64px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 13px;
    text-align: center;
  }}
  footer a {{ color: var(--accent); text-decoration: none; }}
  footer a:hover {{ text-decoration: underline; }}

  @media (max-width: 600px) {{
    body {{ padding: 32px 18px 64px; }}
    h1 {{ font-size: 26px; }}
    .post {{ padding: 18px 18px; }}
    .post-title {{ font-size: 17px; }}
  }}
</style>
</head>
<body>

<header>
  <h1>{site_title}</h1>
  <p class="site-subtitle">{site_subtitle}</p>
  <p class="site-desc">{site_desc}</p>
  <p class="stats">共 {post_count} 篇 · 最后更新 {build_date}</p>
</header>

<ul class="posts">
{post_list}
</ul>

<footer>
  Built by <a href="https://github.com/hudeqi">hudeqi</a> ·
  Last updated {build_date}
</footer>

</body>
</html>
"""


POST_TEMPLATE = """  <li class="post">
    <a href="{filename}">
      <h2 class="post-title">{title}</h2>
      {subtitle_html}
      <div class="post-meta">
        <span class="post-date">{date}</span>
        {tags_html}
      </div>
    </a>
  </li>"""


def render_post(p):
    subtitle_html = (
        f'<p class="post-subtitle">{p["subtitle"]}</p>' if p["subtitle"] else ""
    )
    tags_html = " ".join(f'<span class="tag">{t}</span>' for t in p["tags"])
    return POST_TEMPLATE.format(
        filename=p["filename"],
        title=p["title"],
        subtitle_html=subtitle_html,
        date=p["date"],
        tags_html=tags_html,
    )


def main():
    posts = collect_posts()
    post_list = "\n".join(render_post(p) for p in posts) or "<li>暂无文章</li>"
    html = HTML_TEMPLATE.format(
        site_title=SITE_TITLE,
        site_subtitle=SITE_SUBTITLE,
        site_desc=SITE_DESC,
        post_count=len(posts),
        post_list=post_list,
        build_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅ Generated {out}  ({len(posts)} posts)")
    for p in posts:
        print(f"   - {p['filename']:<60s}  {p['date']}  {p['title'][:50]}")


if __name__ == "__main__":
    main()
