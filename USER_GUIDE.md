# Reddit需求帖证据整理：用户使用指南

## 它能帮你做什么

导入已有的Reddit Listing数据，或整理自己准备的线索JSON；按已填字段提示重复、缺证据和待核验项目。

## 适合谁

合法研究海外需求的自由职业者、产品研究人员。

## 具体解决什么问题

帖子、链接和原文混在一起，讨论、自我推广与购买请求容易被混为一谈。

**不适合这些目标：**自动抓取Reddit、自动判定真实购买意图、自动私信、保证获得客户。

## 下载与准备

- [打开独立仓库](https://github.com/miaorrr8888-cloud/reddit-lead-harvest)
- [直接下载源码ZIP](https://github.com/miaorrr8888-cloud/reddit-lead-harvest/archive/refs/heads/main.zip)

也可在仓库页面点 Code → Download ZIP。解压后打开包含 SKILL.md、README.md、USER_GUIDE.md 的那层文件夹。不要停在外层目录或只复制一个脚本。

建议使用Windows电脑和Python 3.12；这是本次验证环境。先在该文件夹打开PowerShell，再执行：

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe --version
```

这里直接使用虚拟环境里的Python，不需要运行激活脚本或修改系统执行策略。安装步骤及其他系统说明见[通用安装说明](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/INSTALLATION.md)。

本指南的基础示例只用Python标准库，无需安装第三方Python包。

## 第一次使用：先跑自带示例

审查自带两条合成样例：一条需要进一步人工核验，一条自我推广被排除。

```powershell
.\.venv\Scripts\python.exe scripts/review_leads.py examples/leads.json
```

## 结果怎么看

结果包括 NEEDS_HUMAN_VERIFICATION、EXCLUDED 及原因；缺信息时为 NEEDS_INFORMATION，重复时为DUPLICATE。示例不是实际客户。

## 换成自己的资料

leads数组含 title、evidence_url、evidence_quote、kind，预算缺失保留null。kind先由使用者依据原文标注；脚本不是自动理解所有帖子的分类模型。

先用有权取得的少量帖子内容填写自己的JSON，保留原URL和必要摘录。若已有合法取得的Listing导出，可用 import_reddit_export.py 转换，再人工标注意图。

## 不想手动敲命令：给AI助手的任务

以下任务适用于能读取所选目录、执行本地命令的助手。WorkBuddy需要先确认当前版本的权限与技能启用状态；本项目未完成WorkBuddy实际导入验收。

```text
请先读取我选定文件夹中的 SKILL.md 和 USER_GUIDE.md，只在该项目范围内处理。
审查自带合成线索，解释哪些被排除、哪些缺证据、哪些仍需人工核验。不要自动抓取Reddit或联系任何人。帮我列出之后准备自有合法数据时需要填写的字段。
缺少依赖时先说明用途，优先放进本项目虚拟环境；不要读取其他目录中的密码、密钥或浏览器登录数据。
```

## 常见问题

**已经填了buyer_request还要求人工核验**

这是输入声明，不是核验结论；必须回原帖核对当前情况。

**不知道kind该填什么**

先填unknown并保留原文，避免把不确定的讨论硬标成购买请求。

**找不到文件或脚本**

确认终端当前目录就是包含SKILL.md的技能根目录；路径含空格时加双引号。输出目录已存在时换新名字，不覆盖已有结果。

## 当前能力边界

真实需求、预算、发帖者意图都需继续核验。程序不请求Reddit接口；不得用此工具绕过访问限制。快照示例日期固定，过期HOLD是正常保护。

## 验证范围

本指南示例已在Windows独立副本中运行复核，见[命令复核结果](https://github.com/miaorrr8888-cloud/agent-skills-worklog/blob/main/USER_GUIDES_VERIFICATION.md)。已有回归测试只覆盖被测试行为，不证明真实业务结果。WorkBuddy实际运行、手机端使用和所有系统版本均不在本次已验证范围内。

许可证和素材来源分别见 [LICENSE](LICENSE)、[PROVENANCE.md](PROVENANCE.md)。
