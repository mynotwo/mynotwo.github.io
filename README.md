# mynotwo.github.io

Yu Mao 的个人主页 — Research Scientist @ ByteDance (San Jose),AI infra / neural compression / system efficiency。

🔗 **Live:** [mynotwo.github.io](https://mynotwo.github.io)

## 本地预览与检查

```bash
bundle install      # 首次
bash run_server.sh  # http://127.0.0.1:4000
make check          # 构建 _site，并运行页面检查与 crawler 单元测试
```

`Gemfile.lock` 锁定 github-pages 215，其中 nokogiri 1.13.3 要求 Ruby ≥ 2.6 且 < 3.2；本地用 Ruby 2.6 + Bundler 2.2.19 构建，`.github/workflows/ci.yml` 固定同一 Ruby 版本，在 pull request 上运行同一条 `make check`。

## 改什么、在哪改

| 想改 | 文件 |
|---|---|
| 个人介绍 / 研究兴趣 | `_pages/about.md` |
| Current Work 条目 | `_data/current_work.yml`（模板 `_includes/current-work-item.html`） |
| 论文 | `_data/publications.yml`（模板 `_includes/publication-card.html`） |
| News / Honors | `_data/news.yml` / `_data/awards.yml` |
| Services / Supervision | `_data/services.yml` / `_data/supervision.yml` |
| 站点元信息 / 头像 / 邮箱 / 社交账号 | `_config.yml`（设置 `author.twitter` 后，侧栏出现 X 链接，页面带上 `twitter:site`） |
| 侧栏社交链接的顺序、图标、文字 | `_data/author_links.yml`（模板 `_includes/author-profile.html`） |
| 分享卡片（og:image） | `_data/og_cards.yml` 定义，`make og-cards` 生成 `images/og/*.png`；文章在 front matter 里用 `image:` 指向自己的卡片，未指定时用 `_config.yml` 的 `og_image` |
| 博客分类与订阅 | 研究笔记在 front matter 写 `category: research`，进入 `/feed/research.xml`；`/feed.xml` 含全部文章 |
| 数学公式 | 需要 MathJax 的页面在 front matter 写 `mathjax: true` |
| 顶部导航 | `_data/navigation.yml` |
| 头像 / favicon | `images/` |
| 样式 | `_sass/`，入口 `assets/css/main.scss`；首页组件在 `_sass/_homepage.scss`、`_sass/_current-work.scss`、`_sass/_hushword-tool.scss` |

Google Scholar 引用数由本机 launchd 任务 `com.user.scholar-stats`（`~/Library/LaunchAgents/`）每天本地时间 09:17 采集：`~/.scholar-stats/update.sh` 拉取本仓库 `main` 上的 `google_scholar_crawler/`，运行 `publish.py` 校验并原子写入 `google-scholar-stats` 分支；需要本机开机且 `gh` 已登录，日志在 `~/.scholar-stats/update.log`。GitHub 托管 Ubuntu/macOS runner 当前均收到 Scholar 403，因此 `.github/workflows/google_scholar_crawler.yaml` 保留手动检查入口，不承担每日采集。采集失败保留上次成功数据，主页显示数据日期。

## Acknowledgments

基于 [RayeRen/acad-homepage](https://github.com/RayeRen/acad-homepage.github.io)(MIT License),进一步参考了 academicpages 与 minimal-mistakes。
