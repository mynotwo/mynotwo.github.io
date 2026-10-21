# mynotwo.github.io

Yu Mao 的个人主页 — Research Scientist @ ByteDance (San Jose),AI infra / neural compression / system efficiency。

🔗 **Live:** [mynotwo.github.io](https://mynotwo.github.io)

## 本地预览

```bash
bundle install      # 首次
bash run_server.sh  # http://127.0.0.1:4000
```

## 改什么、在哪改

| 想改 | 文件 |
|---|---|
| 个人介绍 / 论文 / News / Honors | `_pages/about.md` |
| 站点元信息 / 社交链接 / 头像 / 邮箱 | `_config.yml` |
| 顶部导航 | `_data/navigation.yml` |
| 头像 / favicon | `images/` |
| 样式 | `_sass/` |

Google Scholar 引用数由本机 Codex 的“每日更新 Scholar 引用数”任务每天洛杉矶时间 01:17 采集，调用 `google_scholar_crawler/publish.py` 校验并原子写入 `google-scholar-stats` 分支；需要本机和 Codex 保持运行。GitHub 托管 Ubuntu/macOS runner 当前均收到 Scholar 403，因此 `.github/workflows/google_scholar_crawler.yaml` 保留手动检查入口，不承担每日采集。采集失败保留上次成功数据，主页显示数据日期。

## Acknowledgments

基于 [RayeRen/acad-homepage](https://github.com/RayeRen/acad-homepage.github.io)(MIT License),进一步参考了 academicpages 与 minimal-mistakes。
