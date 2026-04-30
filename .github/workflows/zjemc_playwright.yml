name: ZJEMC_Playwright_Update

on:
  workflow_dispatch:

permissions:
  contents: write

jobs:
  crawl:
    runs-on: ubuntu-latest

    steps:
      # 1️⃣ 拉代码
      - name: Checkout repo
        uses: actions/checkout@v4

      # 2️⃣ 安装 Python
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      # 3️⃣ 安装依赖（Playwright核心）
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install playwright pandas requests
          playwright install --with-deps chromium

      # 4️⃣ 运行爬虫
      - name: Run crawler
        run: |
          python zjemc_playwright.py

      # 5️⃣ 提交变更
      - name: Commit changes if any
        run: |
          git config --global user.email "BOT@github.com"
          git config --global user.name "githubBOT"
          git add .
          git diff --cached --quiet || git commit -m "update realtime data"

      # 6️⃣ git状态检查（可选）
      - name: Who am I (git)
        run: |
          git remote -v
          git config --get user.name
          git config --get user.email

      # 7️⃣ 推送
      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GTOKEN }}
