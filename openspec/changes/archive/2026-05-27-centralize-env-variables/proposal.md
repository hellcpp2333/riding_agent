## Why

目前项目的 API key 和敏感配置分散在各个文件中（如 agent.py 直接嵌入 BAIDU_MAPS_API_KEY 到 URL），且环境变量加载方式不一致。需要统一将所有敏感信息放入 `.env` 文件，并通过 `load_dotenv()` 集中管理，提高安全性和可配置性。

## What Changes

- 创建统一的 `.env.example` 模板文件，列出所有必需的环境变量
- 将所有 API key、base URL 移至 `.env` 文件管理
- 使用 `python-dotenv` 在应用启动时加载环境变量
- 添加环境变量验证，缺少必要配置时提供清晰的错误提示

**Breaking Changes**: 
- 用户需要在新环境中配置 `.env` 文件才能运行应用

## Capabilities

### New Capabilities

- **env-management**: 集中化的环境变量管理和加载机制

### Modified Capabilities

- None (implementation detail only, no requirement changes)

## Impact

- **New files**: `.env`, `.env.example`
- **Modified**: `app/agents/agent.py` - 移除硬编码的 BAIDU_MAPS_API_KEY，改用环境变量
- **Modified**: `main.py` - 保持 load_dotenv() 调用，简化 env var 检查逻辑
- **Documentation**: 需要在 README 中添加环境变量配置说明
