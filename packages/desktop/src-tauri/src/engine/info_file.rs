use std::fs;
use std::path::PathBuf;
use serde_json::json;

/// 获取服务信息文件路径
pub fn get_engine_info_file_path() -> Option<PathBuf> {
    #[cfg(target_os = "windows")]
    {
        if let Ok(appdata) = std::env::var("APPDATA") {
            let path = PathBuf::from(appdata).join("openwork");
            return Some(path);
        }
    }

    #[cfg(not(target_os = "windows"))]
    {
        if let Some(home) = dirs::home_dir() {
            let path = home.join(".config").join("openwork");
            return Some(path);
        }
    }

    None
}

/// 写入引擎服务信息到文件
pub fn write_engine_info_file(
    running: bool,
    base_url: Option<&str>,
    port: Option<u16>,
    project_dir: Option<&str>,
) -> Result<(), String> {
    let dir = get_engine_info_file_path().ok_or("Failed to get config directory")?;

    // 确保目录存在
    fs::create_dir_all(&dir).map_err(|e| format!("Failed to create directory: {}", e))?;

    let file_path = dir.join("engine-info.json");

    let info = json!({
        "running": running,
        "base_url": base_url,
        "port": port,
        "project_dir": project_dir,
        "updated_at": chrono::Utc::now().to_rfc3339(),
    });

    let content = serde_json::to_string_pretty(&info)
        .map_err(|e| format!("Failed to serialize: {}", e))?;

    fs::write(&file_path, content)
        .map_err(|e| format!("Failed to write file: {}", e))?;

    Ok(())
}

/// 清除引擎服务信息文件
pub fn clear_engine_info_file() -> Result<(), String> {
    write_engine_info_file(false, None, None, None)
}
