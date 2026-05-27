#!/bin/bash
# 一键发布脚本：重新生成首页 → git add → git commit → git push
# 用法：cd ~/Desktop/AI\ learning && ./publish.sh "我新加了一篇 Ep.5 笔记"

set -e

cd "$(dirname "$0")"

MSG="${1:-update blog}"

echo "📝 [1/3] 生成首页 index.html ..."
python3 build_index.py

echo ""
echo "📦 [2/3] 提交 git ..."
git add -A
if git diff --cached --quiet; then
  echo "   ⚠️  没有任何变化，无需提交"
  exit 0
fi
git commit -m "$MSG"

echo ""
echo "🚀 [3/3] 推送到 GitHub ..."
git push

echo ""
echo "✅ 发布成功！1-2 分钟后访问："
echo "   https://hudeqi.github.io/ai-learning-blog/"
