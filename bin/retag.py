#!/usr/bin/env python3
"""Normalise this site's tag vocabulary.

The Blowfish-era corpus had 357 distinct tags over 847 files, half of them used
once, with English and Chinese posts drifting apart. This maps every one of them
onto a fixed bilingual vocabulary, keeps a translated pair's tag sets identical,
and caps each post at four tags by priority.

    python3 bin/retag.py            # report only
    python3 bin/retag.py --write
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# key -> (Chinese label, English label, tier). Tier 1 is the subject of the
# piece, 2 its craft or domain, 3 the register it is written in; when a post
# carries more than four tags the lower tiers are the ones that go.
VOCAB: dict[str, tuple[str, str, int]] = {
    # -- subjects ---------------------------------------------------------
    "postgresql":   ("PostgreSQL", "PostgreSQL", 1),
    "pigsty":       ("Pigsty", "Pigsty", 1),
    "mysql":        ("MySQL", "MySQL", 1),
    "redis":        ("Redis", "Redis", 1),
    "mongodb":      ("MongoDB", "MongoDB", 1),
    "oracle":       ("Oracle", "Oracle", 1),
    "olap":         ("OLAP", "OLAP", 1),
    "domestic":     ("国产数据库", "Domestic Database", 1),
    "ai":           ("AI", "AI", 1),
    "agent":        ("Agent", "Agent", 1),
    "claude":       ("Claude", "Claude", 1),
    "codex":        ("Codex", "Codex", 1),
    "llm":          ("大模型", "LLM", 1),
    "cloud":        ("云计算", "Cloud", 1),
    "cloudexit":    ("下云", "Cloud-Exit", 1),
    # -- craft and domain -------------------------------------------------
    "database":     ("数据库", "Database", 2),
    "rds":          ("RDS", "RDS", 2),
    "ml":           ("机器学习", "Machine Learning", 2),
    "aliyun":       ("阿里云", "Alibaba Cloud", 2),
    "aws":          ("AWS", "AWS", 2),
    "cloudflare":   ("Cloudflare", "Cloudflare", 2),
    "incident":     ("故障复盘", "Incident", 2),
    "cost":         ("成本", "Cost", 2),
    "objectstore":  ("对象存储", "Object Storage", 2),
    "container":    ("容器化", "Containers", 2),
    "linux":        ("Linux", "Linux", 2),
    "hardware":     ("硬件", "Hardware", 2),
    "pgadmin":      ("PG管理", "PG Admin", 2),
    "pgdev":        ("PG开发", "PG Development", 2),
    "pgeco":        ("PG生态", "PG Ecosystem", 2),
    "pgkernel":     ("PG内核", "PG Kernel", 2),
    "extension":    ("扩展", "Extension", 2),
    "monitoring":   ("监控", "Monitoring", 2),
    "backup":       ("备份", "Backup", 2),
    "performance":  ("性能", "Performance", 2),
    "security":     ("安全", "Security", 2),
    "migration":    ("迁移", "Migration", 2),
    "gis":          ("GIS", "GIS", 2),
    "vector":       ("向量", "Vector", 2),
    "transaction":  ("事务", "Transactions", 2),
    "distributed":  ("分布式系统", "Distributed Systems", 2),
    "architecture": ("架构", "Architecture", 2),
    "swe":          ("软件工程", "Software Engineering", 2),
    "sovereignty":  ("数据主权", "Data Sovereignty", 2),
    "localfirst":   ("本地优先", "Local First", 2),
    "repo":         ("软件仓库", "Repository", 2),
    "tools":        ("工具", "Tools", 2),
    "docs":         ("文档", "Documentation", 2),
    # -- register ---------------------------------------------------------
    "opensource":   ("开源", "Open Source", 3),
    "commentary":   ("技术评论", "Commentary", 3),
    "translation":  ("翻译", "Translation", 3),
    "career":       ("职业", "Career", 3),
    "philosophy":   ("哲学", "Philosophy", 3),
    "society":      ("社会观察", "Society", 3),
    "business":     ("商业", "Business", 3),
    "essay":        ("随笔", "Essay", 3),
    "travel":       ("旅行", "Travel", 3),
}

# Every tag the corpus actually uses, folded onto the vocabulary above.
# Keys are lowercased so case and spacing variants collapse together.
MAP: dict[str, str] = {}


def alias(key: str, *names: str) -> None:
    for n in names:
        MAP[n.lower()] = key


alias("postgresql", "PostgreSQL", "PG", "Postgres")
alias("pigsty", "Pigsty", "PigstyApp", "Pigsty App")
alias("mysql", "MySQL", "MySQL走好", "MSSQL")
alias("database", "数据库", "Database", "databases")
alias("rds", "RDS", "云数据库服务")
alias("redis", "Redis", "Valkey")
alias("mongodb", "MongoDB")
alias("oracle", "Oracle")
alias("olap", "OLAP", "DuckDB", "ClickHouse", "Iceberg", "数据中台", "数据标准",
      "SQLite", "数据建模", "Data Modeling")
alias("domestic", "国产数据库", "Domestic-Database", "Domestic Database", "信创",
      "自主可控", "PolarDB", "IvorySQL", "政府采购", "Xinchang Localization", "Homegrown")
alias("ai", "AI", "AI4DB", "DB4AI")
alias("agent", "Agent", "MCP", "OpenClaw", "ClaudeCode", "Claude Code", "Memory", "记忆")
alias("claude", "Claude", "Anthropic", "Fable")
alias("codex", "Codex", "OpenAI")
alias("llm", "大模型", "LLM", "DeepSeek", "Qwen", "GLM", "AGI", "Open Weights", "开放权重",
      "Hallucination", "幻觉", "Alignment", "Google", "NVIDIA")
alias("ml", "机器学习", "Machine Learning", "JEPA", "强化学习", "Reinforcement Learning",
      "神经网络", "World Models", "世界模型", "Causal Reasoning", "因果推理", "KNN",
      "Recommendation System", "推荐系统")
alias("cloud", "云计算", "Cloud", "Cloud Computing", "云数据库", "Cloud Databases",
      "腾讯云", "Tencent-Cloud", "Tencent Cloud", "华为云", "Huawei-Cloud", "GCP",
      "Serverless", "SaaS", "IAM", "SLA")
alias("cloudexit", "下云", "Cloud-Exit", "Cloud Exit", "DHH", "ECS", "EBS")
alias("aliyun", "阿里云", "Alibaba-Cloud", "Alibaba Cloud", "Aliyun")
alias("aws", "AWS")
alias("cloudflare", "Cloudflare", "CDN", "DNS")
alias("incident", "云故障", "Cloud-Outage", "Cloud Outage", "故障档案", "Incident-Report",
      "CrowdStrike", "数据损坏", "Data-Corruption", "运维踩坑", "Vulnerability", "漏洞修复")
alias("cost", "成本", "Cost", "成本分析", "FinOps", "经济", "Economics", "金融")
alias("objectstore", "对象存储", "Object Storage", "S3", "MinIO", "OSS", "Silo", "JuiceFS",
      "File System", "文件系统", "PGFS")
alias("container", "容器化", "Docker", "Kubernetes", "微服务")
alias("linux", "Linux", "OS", "操作系统", "Operating-System", "Ubuntu", "Debian", "SSH")
alias("hardware", "硬件", "Hardware", "Apple", "龙芯", "LoongArch", "Android")
alias("pgadmin", "PG管理", "PG-Admin", "运维", "DBA", "Administration", "管理",
      "权限", "Permissions", "连接池", "Connection-Pool", "锁", "Lock")
alias("pgdev", "PG开发", "PG-Development", "Development", "SQL", "触发器", "Triggers",
      "函数", "Functions", "GIN", "全文检索", "Full-Text-Search", "时间处理",
      "逻辑复制", "CDC", "编程基础", "字符编码", "Encoding", "Unicode")
alias("pgeco", "PG生态", "PG-Ecosystem", "PG Ecosystem", "生态", "Ecosystem",
      "Supabase", "Omnigres", "DBOS", "会议", "Conference", "社区", "Community")
alias("pgkernel", "PG内核", "PG-Kernel", "并发控制")
alias("extension", "扩展", "Extension", "Extensions")
alias("monitoring", "监控", "Monitoring", "可观测性", "Observability", "Metrics", "指标",
      "Prometheus", "Grafana", "VictoriaMetrics", "Victoria", "OpenTelemetry",
      "Logging", "日志")
alias("backup", "备份", "Backup")
alias("performance", "性能", "Performance", "性能优化", "研发效能", "Productivity", "生产力")
alias("security", "安全", "Security", "Privacy", "隐私")
alias("migration", "迁移", "Migration")
alias("gis", "GIS")
alias("vector", "向量", "Vector", "向量数据库", "Vector-Database")
alias("transaction", "事务", "Transactions", "ACID", "事务隔离", "事务系统")
alias("distributed", "分布式系统", "Distributed Systems", "Distributed", "CAP", "etcd",
      "NewSQL", "Runtime", "区块链")
alias("architecture", "架构", "架构设计", "Architecture", "软件架构", "复杂度", "Complexity")
alias("swe", "软件工程", "Software Engineering", "需求分析", "规约", "Convention",
      "Go", "Rust", "Ruby", "Data", "技术对比")
alias("sovereignty", "数据主权", "Data Sovereignty", "Palantir")
alias("localfirst", "本地优先", "Local First")
alias("repo", "软件仓库", "Package Repository", "Software Distribution", "发行版",
      "Distribution", "打包", "Packaging", "SOW", "供应链", "Supply Chain")
alias("tools", "工具", "Tools", "Tool", "Slack")
alias("docs", "文档", "Documentation", "Hugo", "OINK", "官网", "Website", "写作", "Writing",
      "学术引用", "Academic Citations")
alias("opensource", "开源", "Open Source", "Open-Source", "OpenSource", "许可证", "GPL",
      "商标", "Trademark", "信任", "Trust", "收购")
alias("commentary", "技术评论", "Tech Commentary", "Commentary", "行业洞察", "Industry",
      "Industry Analysis", "科技行业", "Tech Industry", "专栏", "正本清源")
alias("translation", "翻译", "Translation", "DDIA")
alias("career", "职业", "职业发展", "Careers", "职场文化", "面试", "Interview",
      "程序员", "Programmers", "就业", "Employment", "大厂", "Big Tech", "学习方法")
alias("philosophy", "哲学", "Philosophy", "本体论", "Ontology", "认知", "Cognition",
      "意识", "Consciousness", "媒介理论", "Media Theory", "麦克卢汉", "Marshall McLuhan",
      "Religion", "思维方式", "认知图景", "Mental Maps", "默会知识", "Tacit Knowledge",
      "小脑", "Cerebellum", "情绪", "Emotion")
alias("society", "社会观察", "Society", "技术变革", "Technological Change", "分配",
      "社会资本", "Social Capital", "自动驾驶", "Autonomous Driving", "未来", "Future")
alias("business", "商业", "Business", "创业", "Startup", "支付宝", "Alipay", "闲鱼",
      "Xianyu", "小红书", "RedNote", "故事", "Story")
alias("travel", "旅行", "Travel", "加拿大", "Canada", "蒙特利尔", "Montreal")

# A post that ends up with nothing keeps its column's own subject.
SECTION_FLOOR = {
    "pg": "postgresql", "db": "database", "cloud": "cloud", "ai": "ai",
    "pigsty": "pigsty", "misc": "essay", "trip": "travel",
}

TAGS_RE = re.compile(r"^tags:\s*(\[.*?\]|)\s*$", re.M)


def split_front_matter(text: str):
    if not text.startswith("---\n"):
        return None, None, None
    end = text.find("\n---", 4)
    if end == -1:
        return None, None, None
    nl = text.find("\n", end + 1)
    return text[4:end], text[end:nl + 1], (text[nl + 1:] if nl != -1 else "")


def read_tags(fm: str) -> list[str]:
    m = TAGS_RE.search(fm)
    if not m or not m.group(1):
        return []
    inner = m.group(1)[1:-1]
    return [t.strip().strip("\"'") for t in inner.split(",") if t.strip()]


def write_tags(fm: str, labels: list[str]) -> str:
    line = "tags: [" + ", ".join(labels) + "]"
    if TAGS_RE.search(fm):
        return TAGS_RE.sub(lambda _: line, fm, count=1)
    # Put a new tags line after the summary/description block, else at the end.
    return fm.rstrip("\n") + "\n" + line


def main(argv: list[str]) -> int:
    write = "--write" in argv
    unmapped = Counter()
    final = Counter()
    sizes = Counter()
    changed = 0

    # Group each bundle's language variants so a pair shares one tag set.
    groups: dict[tuple[str, str], dict[str, Path]] = {}
    for p in sorted(CONTENT.rglob("*.md")):
        if p.name.startswith("_index"):
            continue
        lang = "en" if p.name.endswith(".en.md") else "zh"
        stem = p.name[:-6] if lang == "en" else p.name[:-3]
        groups.setdefault((str(p.parent), stem), {})[lang] = p

    for (_parent, _stem), variants in sorted(groups.items()):
        keys: list[str] = []
        section = ""
        for lang in ("zh", "en"):
            p = variants.get(lang)
            if not p:
                continue
            rel = p.relative_to(CONTENT).parts
            section = rel[0]
            fm, _, _ = split_front_matter(p.read_text(encoding="utf-8"))
            if fm is None:
                continue
            for raw in read_tags(fm):
                key = MAP.get(raw.lower())
                if key is None:
                    unmapped[raw] += 1
                    continue
                if key not in keys:
                    keys.append(key)

        if not keys:
            floor = SECTION_FLOOR.get(section)
            if floor:
                keys = [floor]

        # Four at most, the highest tiers first, then in the order written.
        keys = [k for _, _, k in sorted(
            ((VOCAB[k][2], i, k) for i, k in enumerate(keys)))][:4]

        sizes[len(keys)] += 1
        for k in keys:
            final[k] += 1

        for lang, p in variants.items():
            text = p.read_text(encoding="utf-8")
            fm, sep, body = split_front_matter(text)
            if fm is None:
                continue
            labels = [VOCAB[k][0 if lang == "zh" else 1] for k in keys]
            new_fm = write_tags(fm, labels)
            if new_fm != fm:
                changed += 1
                if write:
                    p.write_text("---\n" + new_fm + sep + body, encoding="utf-8")

    verb = "rewrote" if write else "would rewrite"
    print(f"{verb} {changed} files across {len(groups)} bundles")
    print(f"vocabulary: {len(VOCAB)} tags per language")
    print("tags per post:", dict(sorted(sizes.items())))
    if unmapped:
        print(f"\nUNMAPPED ({len(unmapped)} distinct) -- these would be dropped:")
        for t, c in unmapped.most_common():
            print(f"  {c:4d}  {t}")
    print("\nresulting tag frequency:")
    for k, c in final.most_common():
        print(f"  {c:5d}  {VOCAB[k][0]:<12s} / {VOCAB[k][1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
