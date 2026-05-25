#!/usr/bin/env python3
"""
KnowFlow Nexus - 共享层加载器

统一的数据源和配置加载接口。
所有预测系统通过此模块读取 Nexus 共享知识库的数据。

用法:
    from knowflow_nexus.scripts.loader import get_data_source, get_domain_config
"""

import json
import os
from typing import Any, Optional

NEXUS_DIR = os.path.expanduser("~/knowflow-nexus")
REGISTRY_DIR = os.path.join(NEXUS_DIR, "registry")
CONFIG_DIR = os.path.join(REGISTRY_DIR, "domain-configs")


def get_data_source(source_id: str) -> Optional[dict]:
    """按 ID 查询数据源信息
    
    从 data-sources.json 中查询数据源的访问方式、配置和踩坑记录。
    
    Args:
        source_id: 数据源唯一标识，如 "thesportsdb-free-api", "tencent-finance-api"
    
    Returns:
        数据源字典，若未找到返回 None
    
    示例:
        source = get_data_source("thesportsdb-free-api")
        base_url = source["url"]  # "https://www.thesportsdb.com/api/v1/json/3"
    """
    path = os.path.join(REGISTRY_DIR, "data-sources.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        sources = json.load(f)
    return next((s for s in sources if s["id"] == source_id), None)


def get_all_sources(domain: str = None) -> list[dict]:
    """获取数据源列表，可选按领域过滤
    
    Args:
        domain: 领域标签，如 "football", "stock", "gaokao"
    
    Returns:
        数据源列表
    """
    path = os.path.join(REGISTRY_DIR, "data-sources.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        sources = json.load(f)
    if domain:
        return [s for s in sources if domain in s.get("domains", [])]
    return sources


def get_domain_config(domain: str, config_key: str = None) -> Any:
    """获取领域特定配置
    
    从 domain-configs/{domain}.json 读取领域配置。
    
    Args:
        domain: 领域名，如 "football", "stock", "gaokao"
        config_key: 配置键名。为 None 时返回整个配置字典
    
    Returns:
        配置值，若文件不存在返回 None
    
    示例:
        leagues = get_domain_config("football", "leagues")
        # {"4328": "英超", "4331": "德甲", ...}
    """
    path = os.path.join(CONFIG_DIR, f"{domain}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        config = json.load(f)
    if config_key:
        return config.get(config_key)
    return config


def get_parser_recipe(recipe_id: str) -> Optional[dict]:
    """按 ID 查询解析器配方"""
    path = os.path.join(REGISTRY_DIR, "parser-recipes.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        recipes = json.load(f)
    return next((r for r in recipes if r["id"] == recipe_id), None)


def resolve_endpoint(source_id: str, endpoint_name: str, **params) -> Optional[str]:
    """解析数据源的完整 API URL
    
    从数据源的 endpoints 配置中展开完整 URL。
    
    Args:
        source_id: 数据源 ID
        endpoint_name: 端点名，如 "events_day", "league_table"
        **params: URL 模板参数
    
    Returns:
        完整 URL，若未找到返回 None
    
    示例:
        url = resolve_endpoint("thesportsdb-free-api", "events_day",
                              date="2026-05-25")
        # → "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=2026-05-25&s=Soccer"
    """
    source = get_data_source(source_id)
    if not source or "endpoints" not in source:
        return None
    
    endpoint_tpl = source["endpoints"].get(endpoint_name)
    if not endpoint_tpl:
        return None
    
    base_url = source["url"].rstrip("/")
    path = endpoint_tpl.format(**params)
    return f"{base_url}{path}"
