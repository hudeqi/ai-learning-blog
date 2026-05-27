# dekiehu 的 AI 学习博客

线上地址：https://hudeqi.github.io/ai-learning-blog/

## 写新博客流程

```bash
cd ~/Desktop/AI\ learning/

# 1. 把新写的 HTML 放进当前目录（命名建议：05-xxx.html）

# 2. 发布
./publish.sh "新增 Ep.5 Let's build GPT 笔记"
```

完事。

## 本地预览（不发布）

```bash
python3 build_index.py
open index.html
```

## 文件命名约定

- 文章 HTML 命名：`<序号>-<英文标识>.html`
  - 例：`05-karpathy-letsbuildgpt.html`
  - 序号决定首页排序
- 文章页面里的 `<title>` 会被自动抽到首页作为标题
- 文章页面里的 `<div class="subtitle">...</div>` 会被作为副标题
- 文章页面里的 `<span class="tag">...</span>` 会被作为标签

## 不要做的事

- ❌ 不要手动改 `index.html`（每次 `publish.sh` 会重新生成覆盖）
- ❌ 不要把 `index.html` 当文章源——它只是首页
