# Reddit 需求证据整理

[新手逐步使用指南](USER_GUIDE.md) · [用途与适用人群介绍](INTRODUCTION.md)

`reddit-lead-harvest` · 独立技能仓库 · MIT

适合：研究海外需求的自由职业者、产品开发者

## 解决什么问题

把帖子中的购买请求与同行自我推广分开，保留原帖、原文和缺失项，减少把讨论误当客户的错误。

## 快速开始

Python 3.10+，标准库。无需 API key。

在本仓库根目录运行：

```sh
python scripts/review_leads.py examples/leads.json
```

## 输入与输出

**输入**：JSON 顶层 leads 数组；每项填写 title、evidence_url、evidence_quote、kind。kind 可为 buyer_request、self_promotion、discussion、recruitment、unknown。预算缺失保留 null。

**输出**：JSON 报告：NEEDS_HUMAN_VERIFICATION、NEEDS_INFORMATION、EXCLUDED 或 DUPLICATE；不会产生 VERIFIED、CONTACTED 或成交结论。

## 本次完善

原有缺口：原来只有操作说明，没有可运行的数据整理样例。

已补：新增离线导入检查：标记缺证据、自我推销、重复、预付款请求和待核验状态；提供合成数据与测试。

## 当前限制

导出必须来自本人获准使用的数据；不自动抓取或绕过 API 审批。正文出现某句话不等于需求真实，预算和意图仍需人工复核。删除内容应同步从自有工作副本中移除。

## 验证与使用注意

```sh
python -m unittest discover -s tests -v
```

测试覆盖被断言的离线行为，不等于真实平台、生产模型或业务效果验证。

示例数据和图片均为合成演示，不是真实客户、交易、销量或模型成绩。不要提交真实凭据和私有输入。

## 来源与工作记录

由 miaorrr8888-cloud 在 AI 辅助下积累和维护，来源与边界见 [PROVENANCE.md](PROVENANCE.md)，许可见 [LICENSE](LICENSE)。

[全部独立技能与阶段性工作记录](https://github.com/miaorrr8888-cloud/agent-skills-worklog)

## 第二轮：原始导出与页面证据检查

新增 Reddit Listing JSON 导入，保留未知购买意图；新增本地页面快照摘录匹配、哈希和时效检查。

在仓库根目录运行：

```sh
python scripts/import_reddit_export.py examples/reddit-listing.json
python scripts/review_snapshot.py examples/snapshot.json
```

新增工具的输入字段见脚本参数与 examples/。快照示例采用固定日期，过期后正常返回 HOLD；需要检查新采集的页面时填写真实带时区的采集时间，不要改日期伪装新证据。

## 接入依据

[Reddit 官方 Data API 说明](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)。自动取得数据必须满足平台批准与使用条件，当前导入器不发网络请求。
