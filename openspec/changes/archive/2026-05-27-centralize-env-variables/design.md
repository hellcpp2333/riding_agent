## Context

当前项目的环境变量管理存在以下问题：

1. **分散加载**：`agent.py` 和 `main.py` 各自直接访问环境变量，没有统一入口
2. **硬编码敏感信息**：`BAIDU_MAPS_API_KEY` 被直接嵌入到 BAIDU_MCP_URL 字符串中
3. **缺少验证**：缺少对必需环境变量的统一验证机制
4. **.env 文件不透明**：`.env.example` 模板不存在，新开发者不清楚需要哪些配置

## Goals / Non-Goals

**Goals:**
- 所有 API key 和 base URL 统一管理在 `.env` 文件中
- 应用启动时统一通过 `load_dotenv()` 加载环境变量
- 添加环境变量缺失时的友好错误提示
- 创建 `.env.example` 模板方便新用户配置

**Non-Goals:**
- 不改变应用的外部功能行为
- 不引入新的配置格式（如 yaml/toml）
- 不添加加密或密钥管理服务

## Decisions

1. **统一加载入口**：在 `main.py` 顶部调用 `load_dotenv()`，作为应用的统一入口
2. **环境变量验证函数**：在单独模块中创建 `check_required_env_vars()` 函数，在启动时验证所有必需变量
3. **必需变量清单**：
   - `OPENAI_API_KEY` - LLM API 密钥
   - `OPENAI_BASE_URL` - OpenAI 兼容 API 地址（默认 https://api.deepseek.com）
   - `BAIDU_MAPS_API_KEY` - 百度地图 API 密钥
4. **BAIDU_MCP_URL 构建方式**：保持 `f"https://mcp.map.baidu.com/mcp?ak={BAIDU_MAPS_API_KEY}"` 的构建方式，但使用从环境变量读取的 key

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| `.env` 文件被意外提交到 git | 添加 `.gitignore` 确保 `.env` 不被提交，只提交 `.env.example` |
| 环境变量在模块导入时被访问 | 确保 `load_dotenv()` 在应用启动流程中最早执行 |
| 多开发者配置不一致 | 通过 `.env.example` 提供统一的配置模板和文档 |

## Migration Plan

1. 创建/更新 `.env.example` 文件列出所有环境变量
2. 修改 `main.py` 添加环境变量验证
3. 修改 `agent.py` 移除硬编码和冗余的 env 访问逻辑
4. 测试应用启动正常
