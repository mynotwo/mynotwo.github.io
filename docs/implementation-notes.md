# Implementation Notes — Personal Blog Module

新增「结合式博客」模块：首页「最近文章」区块 + 独立 `/blog/` 子站（列表页 + 独立文章页），中英双语排版 + Giscus 评论。

## 新增文件
- `_posts/2026-06-07-hello-blog.md`、`_posts/2026-06-05-on-learned-compression.md` — 示例文章（一中一英，用于演示语言筛选）
- `_layouts/post.html` — 单篇文章布局（meta + 阅读量 + tags + 上下篇导航 + 返回 + 评论）
- `_layouts/blog.html` — 列表页布局（卡片流 + All/中文/EN 语言筛选，纯 JS 客户端过滤）
- `_pages/blog.md` — `permalink: /blog/`，套 `blog.html`
- `_includes/post-card.html` — 文章卡片（列表页 + 首页复用，视觉仿 `publication-card.html` 的 `.paper-box`）
- `_includes/comments.html` — Giscus 评论区

## 改动文件
- `_data/navigation.yml` — 导航加 `Blog → /blog/`（真实页面，区别于其它 `/#锚点`）
- `_pages/about.md` — News 与 Publications 之间插入 `# 📔 Blog` 区块（最近 3 篇 + View all）
- `_config.yml` — ① 加 posts 的 `defaults`（默认套 post 布局）；② `permalink` 改为 `/blog/:year/:month/:title/`（仅影响 posts，pages 各有自己的 permalink）；③ 加 `giscus:` 配置块
- `assets/css/main.scss` — 末尾追加博客样式（沿用站点既有「内联进 main.scss」的习惯，未另建 `_blog.scss`）

## spec 之外、我自己做的决定
1. **分页**：`jekyll-paginate` v1 对非 `index.html` 的自定义页面分页有坑，学术博客文章量小，**列表页全量渲染 + 客户端语言筛选，不接分页**。文章超过 ~20 篇再考虑。
2. **标签**：用列表页内 JS 客户端筛选思路，**未建每个 tag 的独立归档页**（零维护）。当前 UI 只做了语言筛选；tag 只展示不可点，按需再加。
3. **样式落点**：博客 CSS 直接追加进 `assets/css/main.scss` 末尾，跟现有 `.paper-box` 等自定义样式同一处，而非新建 `_sass/_blog.scss` + import。
4. **示例文章放了 2 篇**（中/英各一），为的是能直观验证语言筛选；不需要可删。

## 相对设计 spec 的额外改动（被迫修的 base-url bug）
站点原本是**单页**，所有静态资源在 `_includes` 里用的是**相对路径**（`assets/css/main.css`、`images/icon.jpg` 等）。一旦引入 `/blog/` 这类嵌套页面，相对路径会解析成 `/blog/assets/...` 全部 404、页面变裸 HTML。已把以下文件的资源路径改成根绝对路径（`/` 开头，本站 baseurl 为空）：
- `_includes/head.html`（main.css）
- `_includes/scripts.html`（main.min.js）
- `_includes/head/custom.html`（icon.jpg ×3、site.webmanifest、mstile、browserconfig、academicons.css）
- `_includes/author-profile.html`（头像 `author.avatar` 加 `replace_first: './', '/'`）

这是博客能在子路径正常工作的**前置必要修复**，不只是博客模块本身。

## 踩坑：`.post-nav` 塌成 0 宽
单篇页「上一篇/下一篇」导航的块级 flex 容器 `.post-nav` 在本模板环境下计算出 `width: 0`（祖先都是 705px 正常宽，唯独它塌 0，唯一命中的就是自己的规则；疑似与 `layout: compress` + head 里那段非法嵌套 `<head><base></head>` 有关）。表现为「上一篇」标题被挤成竖排窄列浮到右上角。
**修法**：`.post-nav` 显式加 `width: 100%; flex-wrap: wrap;`（浏览器实测从 0 → 705，链接回到左侧正常位置）。

## 唯一的手动步骤（OAuth 代不了）
Giscus 评论要生效，需安装 Giscus GitHub App 到本仓库：https://github.com/apps/giscus → Install → 选 `mynotwo/mynotwo.github.io`。
- 仓库 Discussions 已用 `gh repo edit --enable-discussions` 开启。
- `_config.yml` 的 giscus repo_id / category_id 已通过 GitHub GraphQL API 填好（用 Announcements 分类）。
- 装 App 前，文章底部评论区会显示 `giscus is not installed on this repository`；装完即变为可用评论框。

## 本地预览
系统 Ruby 2.6，bundler 用户级装在 `~/.gem`：
```
export GEM_HOME="$HOME/.gem" && export PATH="$HOME/.gem/bin:$PATH"
bundle _2.2.19_ exec jekyll serve --port 4123
```

## 2026-07-02 浏览量统计补丁

线上 `https://mynotwo.github.io/blog/2026/07/in-between/` 没显示浏览量的原因是：当前本地工作区落后于 `origin/main`，本地之前验证的是旧的 `hello-blog` 文章，最新线上文章 `_posts/2026-07-01-in-between.md` 只在远端分支里。

这次基于最新 `origin/main` 新建干净 worktree 后补丁：
- `_config.yml` 增加 `page_views` 配置，provider 使用 Busuanzi。
- `_includes/view-count.html` 输出文章单页浏览数占位。
- `_includes/view-count-script.html` 统一加载 Busuanzi 脚本。
- `_includes/scripts.html` 引入浏览量脚本。
- `_layouts/post.html` 在文章 meta 里显示单篇 views。
- `_pages/about.md` 在 Google Scholar 下方显示全站 Views / Visitors。
- `assets/css/main.scss` 增加轻量样式，保持现有博客视觉。

取舍：Busuanzi 是前端异步计数，静态 HTML 只能验证脚本和占位存在；真实数字需要部署后浏览器成功加载第三方脚本才会填充。

## 2026-07-02 去掉主页全站浏览量

按用户要求移除首页 Google Scholar 下方的全站 `Views / Visitors` 展示，并让 Busuanzi 脚本只在博客文章页加载，只保留单篇 `views`。
