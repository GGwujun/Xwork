use tauri::State;
use crate::engine::manager::EngineManager;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct OpencodeServiceInfo {
    pub running: bool,
    pub base_url: Option<String>,
    pub port: Option<u16>,
    pub project_dir: Option<String>,
}

/// 获取OpenCode服务信息，供外部后端使用
#[tauri::command]
pub fn get_opencode_service_info(manager: State<EngineManager>) -> OpencodeServiceInfo {
    let state = manager.inner.lock().expect("engine mutex poisoned");

    let running = state.child.is_some();

    OpencodeServiceInfo {
        running,
        base_url: state.base_url.clone(),
        port: state.port,
        project_dir: state.project_dir.clone(),
    }
}

/// 通过HTTP暴露OpenCode服务信息
/// 这样Python后端可以通过HTTP请求获取
pub async fn start_bridge_server(manager: State<'_, EngineManager>) -> Result<(), String> {
    // 这里可以启动一个简单的HTTP服务器
    // 监听在固定端口（如8001），提供OpenCode服务信息
    Ok(())
}
