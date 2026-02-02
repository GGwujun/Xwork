#!/usr/bin/env pwsh
#Requires -Version 7.0
<#
.SYNOPSIS
    Git Worktree + VS Code + Claude Code 完整管理脚本
.DESCRIPTION
    交互式创建、管理和销毁 Git Worktree，每个 worktree 都有独立的 VS Code 窗口和 Claude Code 会话
.AUTHOR
    OpenClaw Assistant
.VERSION
    1.0
#>

# 设置严格的错误处理
$ErrorActionPreference = "Stop"

# 颜色配置（用于区分不同 worktree）
$Global:Colors = @(
    @{ Name = "Blue"; Hex = "#1e3a8a"; RGB = @(30, 58, 138) },
    @{ Name = "Red"; Hex = "#7f1d1d"; RGB = @(127, 29, 29) },
    @{ Name = "Green"; Hex = "#14532d"; RGB = @(20, 83, 45) },
    @{ Name = "Purple"; Hex = "#581c87"; RGB = @(88, 28, 135) },
    @{ Name = "Orange"; Hex = "#9a3412"; RGB = @(154, 52, 18) },
    @{ Name = "Teal"; Hex = "#134e4a"; RGB = @(19, 78, 74) },
    @{ Name = "Pink"; Hex = "#831843"; RGB = @(131, 24, 67) },
    @{ Name = "Indigo"; Hex = "#312e81"; RGB = @(49, 46, 129) },
    @{ Name = "Cyan"; Hex = "#164e63"; RGB = @(22, 78, 99) },
    @{ Name = "Amber"; Hex = "#78350f"; RGB = @(120, 53, 15) }
)

$Global:UsedColors = @()

# 图标映射
$Global:Icons = @{
    "feature" = "🚀"
    "bugfix" = "🐛"
    "hotfix" = "🔥"
    "refactor" = "🔧"
    "review" = "👀"
    "docs" = "📝"
    "test" = "🧪"
    "chore" = "📦"
    "experiment" = "🧪"
    "default" = "📁"
}

function Get-RandomColor {
    <#
    .SYNOPSIS
        获取一个未使用的随机颜色
    #>
    $availableColors = $Global:Colors | Where-Object { $_.Name -notin $Global:UsedColors }
    
    if ($availableColors.Count -eq 0) {
        Write-Warning "所有颜色已用完，重置颜色池"
        $Global:UsedColors = @()
        $availableColors = $Global:Colors
    }
    
    $selected = $availableColors | Get-Random
    $Global:UsedColors += $selected.Name
    return $selected
}

function Get-IconForType {
    <#
    .SYNOPSIS
        根据分支类型获取图标
    #>
    param([string]$Type)
    
    $key = $Type.ToLower()
    if ($Global:Icons.ContainsKey($key)) {
        return $Global:Icons[$key]
    }
    return $Global:Icons["default"]
}

function Show-Menu {
    <#
    .SYNOPSIS
        显示主菜单
    #>
    Clear-Host
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║     🌲 Git Worktree + VS Code + Claude Code 管理工具         ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

    Write-Host "请选择操作：" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] 🚀 创建新的 Worktree（开发新功能）" -ForegroundColor Green
    Write-Host "  [2] 📋 列出所有 Worktree" -ForegroundColor White
    Write-Host "  [3] 🔄 合并 Worktree 到主分支" -ForegroundColor Blue
    Write-Host "  [4] 🗑️  销毁 Worktree" -ForegroundColor Red
    Write-Host "  [5] 🧹 清理已不存在的 Worktree 记录" -ForegroundColor Magenta
    Write-Host "  [6] 💻 启动 VS Code + Claude Code" -ForegroundColor Cyan
    Write-Host "  [0] ❌ 退出" -ForegroundColor Gray
    Write-Host ""
}

function Get-MainRepository {
    <#
    .SYNOPSIS
        获取主仓库路径
    #>
    $currentDir = Get-Location
    
    # 检查当前目录是否是 git 仓库
    try {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($gitRoot) {
            return $gitRoot
        }
    } catch {
        # 不是 git 仓库
    }
    
    # 询问用户
    Write-Host "⚠️  当前目录不是 Git 仓库" -ForegroundColor Yellow
    $path = Read-Host "请输入主 Git 仓库路径"
    
    if (-not (Test-Path $path)) {
        throw "路径不存在: $path"
    }
    
    if (-not (Test-Path (Join-Path $path ".git"))) {
        throw "指定路径不是 Git 仓库"
    }
    
    return (Resolve-Path $path).Path
}

function New-Worktree {
    <#
    .SYNOPSIS
        创建新的 Git Worktree
    #>
    param(
        [string]$RepoPath
    )
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "        🚀 创建新的 Git Worktree" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    # 获取分支类型
    Write-Host "选择分支类型：" -ForegroundColor Yellow
    Write-Host "  1. feature  - 新功能开发"
    Write-Host "  2. bugfix   - 缺陷修复"
    Write-Host "  3. hotfix   - 紧急修复"
    Write-Host "  4. refactor - 代码重构"
    Write-Host "  5. docs     - 文档更新"
    Write-Host "  6. test     - 测试相关"
    Write-Host "  7. review   - 代码审查"
    Write-Host "  8. other    - 其他"
    Write-Host ""
    
    $typeChoice = Read-Host "请输入类型编号 (1-8)"
    
    $branchType = switch ($typeChoice) {
        "1" { "feature" }
        "2" { "bugfix" }
        "3" { "hotfix" }
        "4" { "refactor" }
        "5" { "docs" }
        "6" { "test" }
        "7" { "review" }
        default { "feature" }
    }
    
    # 获取分支名称
    $branchName = Read-Host "请输入分支名称（如: user-dashboard, api-optimization）"
    
    if ([string]::IsNullOrWhiteSpace($branchName)) {
        throw "分支名称不能为空"
    }
    
    # 清理分支名称
    $branchName = $branchName -replace '\s+', '-'
    $branchName = $branchName -replace '[^a-zA-Z0-9\-_]', ''
    $fullBranchName = "$branchType/$branchName"
    
    # 获取描述
    $description = Read-Host "请输入简短描述（可选，用于 Claude Code 上下文）"
    if ([string]::IsNullOrWhiteSpace($description)) {
        $description = "开发 $branchType/$branchName"
    }
    
    # 生成 worktree 名称
    $repoName = Split-Path $RepoPath -Leaf
    $worktreeName = "$repoName-$branchType-$branchName"
    $worktreePath = Join-Path (Split-Path $RepoPath -Parent) $worktreeName
    
    # 检查路径是否已存在
    if (Test-Path $worktreePath) {
        $overwrite = Read-Host "⚠️  Worktree 路径已存在。是否删除并重建？(y/N)"
        if ($overwrite -eq 'y' -or $overwrite -eq 'Y') {
            Remove-Item -Path $worktreePath -Recurse -Force
        } else {
            Write-Host "❌ 已取消" -ForegroundColor Red
            return
        }
    }
    
    # 获取随机颜色
    $color = Get-RandomColor
    $icon = Get-IconForType $branchType
    
    Write-Host ""
    Write-Host "📋 创建信息确认：" -ForegroundColor Cyan
    Write-Host "  分支类型: $icon $branchType"
    Write-Host "  分支名称: $fullBranchName"
    Write-Host "  工作目录: $worktreePath"
    Write-Host "  标识颜色: $($color.Name) $($color.Hex)"
    Write-Host "  描述: $description"
    Write-Host ""
    
    $confirm = Read-Host "确认创建？(Y/n)"
    if ($confirm -eq 'n' -or $confirm -eq 'N') {
        Write-Host "❌ 已取消" -ForegroundColor Red
        return
    }
    
    # 切换到主仓库目录
    Push-Location $RepoPath
    
    try {
        # 检查分支是否已存在
        $branchExists = git branch --list $fullBranchName | Select-String $fullBranchName
        
        if ($branchExists) {
            Write-Host "⚠️  分支 $fullBranchName 已存在，直接检出..." -ForegroundColor Yellow
            git worktree add "$worktreePath" $fullBranchName
        } else {
            Write-Host "🌱 创建新分支并建立 worktree..." -ForegroundColor Green
            git worktree add -b $fullBranchName "$worktreePath"
        }
        
        Write-Host "✅ Worktree 创建成功！" -ForegroundColor Green
        
        # 创建 VS Code 配置
        New-VSCodeConfig -WorktreePath $worktreePath -BranchName $fullBranchName -BranchType $branchType -Color $color -Description $description -Icon $icon
        
        # 询问是否立即打开 VS Code
        $openNow = Read-Host ""
        $openNow = Read-Host "是否立即在 VS Code 中打开？(Y/n)"
        if ($openNow -ne 'n' -and $openNow -ne 'N') {
            Open-VSCode -Path $worktreePath
        }
        
        Write-Host ""
        Write-Host "🎉 Worktree 创建完成！" -ForegroundColor Green
        Write-Host "   路径: $worktreePath"
        Write-Host "   打开方式: code '$worktreePath'"
        
    } finally {
        Pop-Location
    }
}

function New-VSCodeConfig {
    <#
    .SYNOPSIS
        创建 VS Code 配置文件
    #>
    param(
        [string]$WorktreePath,
        [string]$BranchName,
        [string]$BranchType,
        [hashtable]$Color,
        [string]$Description,
        [string]$Icon
    )
    
    $vscodeDir = Join-Path $WorktreePath ".vscode"
    New-Item -ItemType Directory -Path $vscodeDir -Force | Out-Null
    
    # settings.json
    $settings = @{
        "window.title" = "$Icon $BranchName - `${activeEditorShort}`${separator}`${rootName}"
        "workbench.colorTheme" = "GitHub Dark"
        "workbench.colorCustomizations" = @{
            "titleBar.activeBackground" = $Color.Hex
            "titleBar.activeForeground" = "#ffffff"
            "titleBar.inactiveBackground" = $Color.Hex
            "titleBar.inactiveForeground" = "#cccccc"
            "activityBar.background" = $Color.Hex
            "activityBar.foreground" = "#ffffff"
        }
        "claude.code.workspace" = $BranchName
        "claude.code.context" = $Description
        "terminal.integrated.defaultProfile.windows" = "PowerShell"
        "terminal.integrated.defaultProfile.osx" = "zsh"
        "terminal.integrated.defaultProfile.linux" = "bash"
        "git.openRepositoryInParentFolders" = "never"
        "files.exclude" = @{
            "**/.git" = $true
            "**/node_modules" = $true
            "**/dist" = $true
            "**/build" = $true
        }
    } | ConvertTo-Json -Depth 10
    
    $settings | Out-File -FilePath (Join-Path $vscodeDir "settings.json") -Encoding UTF8
    
    # extensions.json - 推荐扩展
    $extensions = @{
        recommendations = @(
            "anthropic.claude-code"
            "eamodio.gitlens"
            "mhutchie.git-graph"
            "usernamehw.errorlens"
            "streetsidesoftware.code-spell-checker"
        )
    } | ConvertTo-Json -Depth 5
    
    $extensions | Out-File -FilePath (Join-Path $vscodeDir "extensions.json") -Encoding UTF8
    
    # 创建 README.md
    $readme = @"
# $Icon $BranchName

**类型:** $BranchType  
**描述:** $Description  
**颜色:** $($color.Name)  

## 快速开始

```bash
# 在 VS Code 中打开
code .

# 启动 Claude Code
claude
```

## 工作区信息

- 主仓库: $(git -C $WorktreePath rev-parse --show-toplevel 2>$null || "Unknown")
- 当前分支: $(git -C $WorktreePath branch --show-current 2>$null || "Unknown")
- 创建时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 注意事项

⚠️ 这是一个 Git Worktree，与主仓库共享 Git 历史，但工作目录独立。

---
Generated by Git Worktree Manager
"@
    
    $readme | Out-File -FilePath (Join-Path $WorktreePath "WORKTREE_README.md") -Encoding UTF8
    
    Write-Host "📝 VS Code 配置已创建" -ForegroundColor Cyan
}

function Open-VSCode {
    <#
    .SYNOPSIS
        在 VS Code 中打开指定路径
    #>
    param([string]$Path)
    
    if (-not (Get-Command "code" -ErrorAction SilentlyContinue)) {
        throw "VS Code 命令行工具未安装或未添加到 PATH"
    }
    
    Write-Host "💻 启动 VS Code: $Path" -ForegroundColor Cyan
    Start-Process "code" -ArgumentList "$Path"
    Start-Sleep -Seconds 2
}

function Show-Worktrees {
    <#
    .SYNOPSIS
        显示所有 Worktree 列表
    #>
    param([string]$RepoPath)
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "           📋 所有 Git Worktree" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    Push-Location $RepoPath
    try {
        $worktrees = git worktree list --porcelain 2>$null
        
        if (-not $worktrees) {
            Write-Host "⚠️  没有找到 worktree" -ForegroundColor Yellow
            return
        }
        
        $currentEntry = @{}
        $entries = @()
        
        foreach ($line in $worktrees -split "`n") {
            if ($line -match "^worktree (.+)$") {
                if ($currentEntry.Path) {
                    $entries += $currentEntry.Clone()
                }
                $currentEntry = @{ Path = $matches[1]; Branch = ""; Detached = $false }
            }
            elseif ($line -match "^branch (.+)$") {
                $currentEntry.Branch = $matches[1] -replace "refs/heads/", ""
            }
            elseif ($line -match "^detached") {
                $currentEntry.Detached = $true
            }
        }
        
        if ($currentEntry.Path) {
            $entries += $currentEntry
        }
        
        # 打印表格
        Write-Host "┌──────────────────────────────────────────────────────────────────────────────┐"
        Write-Host "│ 路径                              │ 分支                    │ 状态           │"
        Write-Host "├──────────────────────────────────────────────────────────────────────────────┤"
        
        foreach ($entry in $entries) {
            $path = $entry.Path
            if ($path.Length -gt 35) {
                $path = "..." + $path.Substring($path.Length - 32)
            }
            
            $branch = if ($entry.Detached) { "(detached)" } else { $entry.Branch }
            if ($branch.Length -gt 23) {
                $branch = $branch.Substring(0, 20) + "..."
            }
            
            $status = if (Test-Path $entry.Path) { "✅ 正常" } else { "❌ 缺失" }
            
            Write-Host "│ $("{0,-35}" -f $path) │ $("{0,-23}" -f $branch) │ $("{0,-14}" -f $status) │"
        }
        
        Write-Host "└──────────────────────────────────────────────────────────────────────────────┘"
        Write-Host ""
        Write-Host "共 $($entries.Count) 个 worktree"
        
    } finally {
        Pop-Location
    }
}

function Merge-Worktree {
    <#
    .SYNOPSIS
        合并 Worktree 到主分支
    #>
    param([string]$RepoPath)
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Blue
    Write-Host "         🔄 合并 Worktree 到主分支" -ForegroundColor Blue
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Blue
    Write-Host ""
    
    # 列出所有 worktree
    Push-Location $RepoPath
    $worktrees = @(git worktree list --porcelain 2>$null | Select-String "^worktree (.+)$" | ForEach-Object { $_.Matches.Groups[1].Value })
    Pop-Location
    
    if ($worktrees.Count -eq 0) {
        Write-Host "⚠️  没有找到 worktree" -ForegroundColor Yellow
        return
    }
    
    Write-Host "选择要合并的 Worktree：" -ForegroundColor Yellow
    for ($i = 0; $i -lt $worktrees.Count; $i++) {
        Write-Host "  [$($i + 1)] $($worktrees[$i])"
    }
    Write-Host ""
    
    $choice = Read-Host "请输入编号 (1-$($worktrees.Count))"
    $index = [int]$choice - 1
    
    if ($index -lt 0 -or $index -ge $worktrees.Count) {
        Write-Host "❌ 无效选择" -ForegroundColor Red
        return
    }
    
    $worktreePath = $worktrees[$index]
    $branchName = git -C $worktreePath branch --show-current 2>$null
    
    Write-Host ""
    Write-Host "📋 合并信息：" -ForegroundColor Cyan
    Write-Host "  Worktree: $worktreePath"
    Write-Host "  分支: $branchName"
    Write-Host ""
    
    Write-Host "合并选项：" -ForegroundColor Yellow
    Write-Host "  1. merge    - 合并到当前分支（保留提交历史）"
    Write-Host "  2. squash   - 压缩合并（所有变更合并为一个提交）"
    Write-Host "  3. rebase   - 变基合并（线性历史）"
    Write-Host "  4. cancel   - 取消"
    Write-Host ""
    
    $mergeType = Read-Host "请选择合并方式 (1-4)"
    
    Push-Location $RepoPath
    
    try {
        switch ($mergeType) {
            "1" {
                Write-Host "🔄 执行 merge..." -ForegroundColor Blue
                git merge $branchName --no-edit
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Merge 成功！" -ForegroundColor Green
                }
            }
            "2" {
                Write-Host "🔄 执行 squash merge..." -ForegroundColor Blue
                git merge --squash $branchName
                if ($LASTEXITCODE -eq 0) {
                    $message = Read-Host "请输入提交信息"
                    if ([string]::IsNullOrWhiteSpace($message)) {
                        $message = "Merge $branchName"
                    }
                    git commit -m "$message"
                    Write-Host "✅ Squash merge 成功！" -ForegroundColor Green
                }
            }
            "3" {
                Write-Host "🔄 执行 rebase..." -ForegroundColor Blue
                git rebase $branchName
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Rebase 成功！" -ForegroundColor Green
                }
            }
            default {
                Write-Host "❌ 已取消" -ForegroundColor Yellow
                return
            }
        }
        
        if ($LASTEXITCODE -eq 0) {
            $cleanup = Read-Host "合并成功！是否删除 worktree？(y/N)"
            if ($cleanup -eq 'y' -or $cleanup -eq 'Y') {
                Remove-Worktree -RepoPath $RepoPath -WorktreePath $worktreePath
            }
        }
        
    } finally {
        Pop-Location
    }
}

function Remove-Worktree {
    <#
    .SYNOPSIS
        删除 Worktree
    #>
    param(
        [string]$RepoPath,
        [string]$WorktreePath = $null
    )
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Red
    Write-Host "           🗑️  销毁 Worktree" -ForegroundColor Red
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Red
    Write-Host ""
    
    Push-Location $RepoPath
    
    try {
        if (-not $WorktreePath) {
            # 列出所有非主 worktree
            $worktrees = @(git worktree list | Select-Object -Skip 1)
            
            if ($worktrees.Count -eq 0) {
                Write-Host "⚠️  没有其他 worktree 可删除" -ForegroundColor Yellow
                return
            }
            
            Write-Host "选择要删除的 Worktree：" -ForegroundColor Yellow
            for ($i = 0; $i -lt $worktrees.Count; $i++) {
                Write-Host "  [$($i + 1)] $($worktrees[$i])"
            }
            Write-Host ""
            
            $choice = Read-Host "请输入编号 (1-$($worktrees.Count))，或输入 0 取消"
            
            if ($choice -eq "0") {
                Write-Host "❌ 已取消" -ForegroundColor Yellow
                return
            }
            
            $index = [int]$choice - 1
            $WorktreePath = ($worktrees[$index] -split "\s+")[0]
        }
        
        Write-Host "⚠️  警告：这将删除以下 worktree 及其所有未提交的更改！" -ForegroundColor Red
        Write-Host "  路径: $WorktreePath"
        Write-Host ""
        
        $confirm = Read-Host "确认删除？(输入 'delete' 确认)"
        
        if ($confirm -ne "delete") {
            Write-Host "❌ 已取消（需要输入 'delete' 确认）" -ForegroundColor Yellow
            return
        }
        
        # 强制删除 worktree
        git worktree remove --force "$WorktreePath" 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Worktree 已删除" -ForegroundColor Green
            
            # 询问是否删除文件夹
            if (Test-Path $WorktreePath) {
                $removeFolder = Read-Host "是否同时删除文件夹？($WorktreePath) (y/N)"
                if ($removeFolder -eq 'y' -or $removeFolder -eq 'Y') {
                    Remove-Item -Path $WorktreePath -Recurse -Force
                    Write-Host "✅ 文件夹已删除" -ForegroundColor Green
                }
            }
            
            # 询问是否删除远程分支
            $branchName = git branch -r | Select-String "origin/(.+)" | ForEach-Object { 
                if ($WorktreePath -match ($_.Matches.Groups[1].Value -replace "/", "-")) {
                    return $_.Matches.Groups[1].Value
                }
            }
            
            if ($branchName) {
                $deleteRemote = Read-Host "是否同时删除远程分支 origin/$branchName？(y/N)"
                if ($deleteRemote -eq 'y' -or $deleteRemote -eq 'Y') {
                    git push origin --delete $branchName
                    Write-Host "✅ 远程分支已删除" -ForegroundColor Green
                }
            }
        } else {
            Write-Host "❌ 删除失败" -ForegroundColor Red
        }
        
    } finally {
        Pop-Location
    }
}

function Prune-Worktrees {
    <#
    .SYNOPSIS
        清理已不存在的 worktree 记录
    #>
    param([string]$RepoPath)
    
    Write-Host ""
    Write-Host "🧹 清理 worktree 记录..." -ForegroundColor Magenta
    
    Push-Location $RepoPath
    try {
        $output = git worktree prune --verbose 2>&1
        Write-Host $output -ForegroundColor Gray
        Write-Host "✅ 清理完成" -ForegroundColor Green
    } finally {
        Pop-Location
    }
}

function Start-VSCodeSessions {
    <#
    .SYNOPSIS
        启动所有 worktree 的 VS Code
    #>
    param([string]$RepoPath)
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "      💻 启动 VS Code + Claude Code" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    Push-Location $RepoPath
    $worktrees = @(git worktree list --porcelain 2>$null | Select-String "^worktree (.+)$" | ForEach-Object { $_.Matches.Groups[1].Value })
    Pop-Location
    
    if ($worktrees.Count -eq 0) {
        Write-Host "⚠️  没有找到 worktree" -ForegroundColor Yellow
        return
    }
    
    Write-Host "找到 $($worktrees.Count) 个 worktree" -ForegroundColor Green
    Write-Host ""
    
    for ($i = 0; $i -lt $worktrees.Count; $i++) {
        $wt = $worktrees[$i]
        $branch = git -C $wt branch --show-current 2>$null
        
        Write-Host "[$($i + 1)/$($worktrees.Count)] 启动: $branch" -ForegroundColor Cyan
        Open-VSCode -Path $wt
        Start-Sleep -Seconds 3  # 间隔启动避免资源竞争
    }
    
    Write-Host ""
    Write-Host "🎉 所有 VS Code 窗口已启动！" -ForegroundColor Green
}

# ════════════════════════════════════════════════════════════
# 主程序入口
# ════════════════════════════════════════════════════════════

function Main {
    try {
        # 获取主仓库路径
        $repoPath = Get-MainRepository
        Write-Host "📁 主仓库: $repoPath" -ForegroundColor Cyan
        Write-Host ""
        
        while ($true) {
            Show-Menu
            $choice = Read-Host "请输入选项 (0-6)"
            
            switch ($choice) {
                "1" { New-Worktree -RepoPath $repoPath }
                "2" { Show-Worktrees -RepoPath $repoPath }
                "3" { Merge-Worktree -RepoPath $repoPath }
                "4" { Remove-Worktree -RepoPath $repoPath }
                "5" { Prune-Worktrees -RepoPath $repoPath }
                "6" { Start-VSCodeSessions -RepoPath $repoPath }
                "0" { 
                    Write-Host ""
                    Write-Host "👋 再见！" -ForegroundColor Cyan
                    exit 0 
                }
                default { 
                    Write-Host "❌ 无效选项，请重试" -ForegroundColor Red
                    Start-Sleep -Seconds 1
                }
            }
            
            Write-Host ""
            Read-Host "按 Enter 键继续"
        }
    }
    catch {
        Write-Host ""
        Write-Host "❌ 错误: $_" -ForegroundColor Red
        Write-Host $_.ScriptStackTrace -ForegroundColor Gray
        exit 1
    }
}

# 运行主程序
Main
