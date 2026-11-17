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
| 站点元信息 / 头像 / 邮箱 / 社交账号 | `_config.yml` |
| 侧栏社交链接的顺序、图标、文字 | `_data/author_links.yml`（模板 `_includes/author-profile.html`） |
| 顶部导航 | `_data/navigation.yml` |
| 头像 / favicon | `images/` |
| 样式 | `_sass/`，入口 `assets/css/main.scss`；首页组件在 `_sass/_homepage.scss`、`_sass/_current-work.scss`、`_sass/_hushword-tool.scss` |

Google Scholar 引用数由本机 Codex 的“每日更新 Scholar 引用数”任务每天洛杉矶时间 01:17 采集，调用 `google_scholar_crawler/publish.py` 校验并原子写入 `google-scholar-stats` 分支；需要本机和 Codex 保持运行。GitHub 托管 Ubuntu/macOS runner 当前均收到 Scholar 403，因此 `.github/workflows/google_scholar_crawler.yaml` 保留手动检查入口，不承担每日采集。采集失败保留上次成功数据，主页显示数据日期。

## Acknowledgments

基于 [RayeRen/acad-homepage](https://github.com/RayeRen/acad-homepage.github.io)(MIT License),进一步参考了 academicpages 与 minimal-mistakes。
