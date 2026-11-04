# Reddit 需求证据整理

[新手逐步使用指南](USER_GUIDE.md) · [用途与适用人群介绍](INTRODUCTION.md)

`reddit-lead-harvest` · 独立技能仓库 · MIT

适合：研究海外需求的自由职业者、产品开发者

## 解决什么问题

把帖子中的购买请求与同行自我推广分开，保留原帖、原文和缺失项，减少把讨论误当客户的错误。

## 安装

```sh
# 纯标准库，不需要任何第三方包，也不需要 API key
python scripts/review_leads.py examples/leads.json
```

作为技能使用时，把整个目录放进 `%USERPROFILE%\.workbuddy\skills\`。

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

## 适用用户

**适合：** 已经有 Reddit 导出文件（自己抓取或平台导出）、想从中筛出真实需求线索的人；
需要保留原文与时间戳以便复核的人。

**不适合：** 想自动发私信/自动联系客户的人（本技能不联系任何人）；
没有导出文件、期待工具自己爬全网的人；以及未经许可抓取他人数据的使用方式。

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

## 许可证

MIT，全文见 [LICENSE](LICENSE)。可商用、可修改、可再分发，保留版权与许可声明即可。

**不提供任何形式的担保。** 本技能输出的是辅助判断，不构成法律、财税或平台合规意见；
线索需人工核实后才可联系，本技能不自动触达任何人。

第三方依赖各自遵循其原始许可证，本项目不再分发它们的代码或模型权重，详见 `PROVENANCE.md`（如有）。

## 运行环境

| 项 | 状态 |
|---|---|
| Windows 11 + Python 3.12 / 3.13 | ✅ 实测通过 |
| Linux / macOS | ⚠️ **未实测**。代码用 `pathlib`，无硬编码分隔符，理论上可跑，但测试只在 Windows 跑过，不声称支持 |

诚实标注：没实跑过的平台，不要在对外文案里写「已支持」。
