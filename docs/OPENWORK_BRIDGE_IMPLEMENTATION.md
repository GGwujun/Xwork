# 方案1：通过OpenWork获取服务URL - 实现文档

## 📋 方案概述

本方案实现了后端与OpenWork的自动通信机制，让后端能够自动获取OpenCode服务的动态URL，无需手动配置。

## 🏗️ 架构设计

### 通信流程

```
OpenWork (Tauri)
    ↓ 写入服务信息
engine-info.json (共享文件)
    ↓ 读取服务信息
Backend (Python)
    ↓ 使用动态URL
OpenCode Service
```

### 核心组件

1. **OpenWork端**：
   - `engine/info_file.rs` - 写入服务信息到文件
   - `commands/engine.rs` - 启动/停止时更新服务信息

2. **Backend端**：
   - `openwork_bridge.py` - 读取OpenWork服务信息
   - `opencode_integration.py` - 集成桥接功能
   - `main.py` - 提供状态查询API

## 📁 文件说明

### 新增文件

1. **backend/app/openwork_bridge.py**
   - OpenWork桥接器
   - 从共享文件读取服务信息
   - 提供OpenCode服务URL

2. **backend/test_openwork_bridge.py**
   - 桥接功能测试脚本
   - 验证完整通信流程

3. **packages/desktop/src-tauri/src/engine/info_file.rs**
   - 服务信息文件管理
   - 写入/清除服务信息

4. **packages/desktop/src-tauri/src/commands/opencode_bridge.rs**
   - Tauri命令接口（备用方案）

### 修改文件

1. **backend/app/opencode_integration.py**
   - 集成OpenWork桥接
   - 支持多种URL获取方式
   - 优先级：参数 > OpenWork > 环境变量 > 默认值

2. **backend/main.py**
   - 新增 `/opencode/status` API
   - 查询OpenCode服务状态

## 🚀 使用方法

### 步骤1：启动OpenWork

```bash
cd E:\winning\code\vue3\openwork
pnpm dev
```

OpenWork启动时会：
1. 自动启动OpenCode服务（动态端口）
2. 将服务信息写入共享文件

### 步骤2：启动后端服务

```bash
cd E:\winning\code\vue3\openwork\backend
python -m uvicorn main:app --reload
```

后端启动时会：
1. 自动从OpenWork读取服务URL
2. 使用动态URL连接OpenCode服务

### 步骤3：验证连接

```bash
# 测试桥接功能
python test_openwork_bridge.py

# 或通过API查询
curl http://127.0.0.1:8000/opencode/status
```

## 📊 服务信息文件

### 文件位置

- **Windows**: `%APPDATA%\openwork\engine-info.json`
- **macOS/Linux**: `~/.config/openwork/engine-info.json`

### 文件格式

```json
{
  "running": true,
  "base_url": "http://127.0.0.1:54321",
  "port": 54321,
  "project_dir": "E:\\workspace\\my-project",
  "updated_at": "2026-02-04T10:30:00Z"
}
```

## 🔄 URL获取优先级

后端按以下优先级获取OpenCode服务URL：

1. **函数参数** - 直接传入URL
2. **OpenWork桥接** - 从共享文件读取
3. **环境变量** - `OPENCODE_URL`
4. **默认值** - `http://127.0.0.1:4096`

## 🧪 测试

### 运行测试脚本

```bash
cd E:\winning\code\vue3\openwork\backend
python test_openwork_bridge.py
```

### 预期输出

```
============================================================
OpenWork桥接功能测试
============================================================

1. 测试OpenWork桥接器...
✅ 成功从OpenWork获取服务信息:
   - 运行状态: True
   - 服务URL: http://127.0.0.1:54321
   - 端口: 54321
   - 项目目录: E:\workspace\my-project
   - 更新时间: 2026-02-04T10:30:00Z

2. 测试OpenCode生成器初始化...
   OpenCode服务URL: http://127.0.0.1:54321

3. 测试OpenCode服务连接...
✅ OpenCode服务连接成功
   健康状态: {'healthy': True, 'version': '1.0.0'}

4. 测试后端API...
✅ 后端API响应成功
   状态: connected
   来源: openwork
   服务信息: {...}

============================================================
测试完成
============================================================
```

## 🔧 故障排查

### 问题1：无法从OpenWork获取服务信息

**症状**：
```
⚠️  无法从OpenWork获取服务信息
```

**解决方案**：
1. 确认OpenWork正在运行
2. 检查服务信息文件是否存在
3. 验证文件权限

### 问题2：OpenCode服务连接失败

**症状**：
```
❌ 无法连接到OpenCode服务
```

**解决方案**：
1. 确认OpenWork已启动OpenCode服务
2. 检查防火墙设置
3. 验证端口未被占用

### 问题3：后端API无响应

**症状**：
```
❌ 无法连接到后端服务
```

**解决方案**：
1. 确认后端服务正在运行
2. 检查端口8000是否被占用
3. 查看后端日志

## 📝 API文档

### GET /opencode/status

获取OpenCode服务状态

**响应示例**：

```json
{
  "status": "connected",
  "source": "openwork",
  "service_info": {
    "running": true,
    "base_url": "http://127.0.0.1:54321",
    "port": 54321,
    "project_dir": "E:\\workspace\\my-project",
    "updated_at": "2026-02-04T10:30:00Z"
  }
}
```

## ✅ 优势

1. **自动化** - 无需手动配置URL
2. **动态适应** - 支持动态端口分配
3. **降级处理** - 支持多种获取方式
4. **易于调试** - 提供状态查询API
5. **向后兼容** - 保持原有API不变

## 🎯 下一步

1. 在OpenWork的Rust代码中集成`info_file.rs`
2. 在`engine_start`和`engine_stop`时调用写入/清除函数
3. 测试完整流程
4. 部署到生产环境

## 📚 相关文件

- `backend/app/openwork_bridge.py` - 桥接器实现
- `backend/app/opencode_integration.py` - 集成代码
- `backend/test_openwork_bridge.py` - 测试脚本
- `packages/desktop/src-tauri/src/engine/info_file.rs` - 文件管理
