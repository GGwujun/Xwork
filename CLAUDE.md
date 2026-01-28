# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenWork is an extensible, open-source "Claude Work" style system for knowledge workers. It's a native desktop app built with Tauri that runs OpenCode under the hood, presenting it as a clean, guided workflow with a premium UI. The goal is to make "agentic work" feel like a product, not a terminal.

## Technology Stack

- **Desktop/Mobile shell**: Tauri 2.x
- **Frontend**: SolidJS + TailwindCSS 4
- **State management**: SolidJS signals + stores
- **OpenCode integration**: `@opencode-ai/sdk` v2 client
- **Package manager**: pnpm (v10.27.0)

## Repository Structure

This is a pnpm monorepo with three main packages:

- `packages/app/` - SolidJS UI application (formerly `openwork-ui`)
- `packages/desktop/` - Tauri desktop shell
- `packages/owpenbot/` - WhatsApp bot bridge (optional)

## Common Commands

### Development
```bash
pnpm dev              # Run desktop app in dev mode
pnpm dev:ui           # Run UI only (web mode)
pnpm dev:web          # Alias for dev:ui
```

### Building
```bash
pnpm build            # Build desktop app
pnpm build:ui         # Build UI only
pnpm build:web        # Alias for build:ui
```

### Testing
```bash
pnpm typecheck        # TypeScript type checking
pnpm test:health      # Health check tests
pnpm test:sessions    # Session management tests
pnpm test:events      # Event streaming tests
pnpm test:todos       # Todo list tests
pnpm test:permissions # Permission flow tests
pnpm test:e2e         # Full end-to-end test suite
pnpm test:refactor    # Quick refactor validation (typecheck + health + sessions)
```

### Version Management
```bash
pnpm bump:patch       # Bump patch version (0.0.X)
pnpm bump:minor       # Bump minor version (0.X.0)
pnpm bump:major       # Bump major version (X.0.0)
pnpm bump:set         # Set specific version
```

### Tauri Commands
```bash
pnpm tauri dev        # Run Tauri dev mode
pnpm tauri build      # Build Tauri app
```

## Architecture

### Two Runtime Modes

1. **Host mode**: OpenWork spawns `opencode serve` locally on `127.0.0.1:<port>` with the selected project folder as working directory
2. **Client mode**: OpenWork connects to an existing OpenCode server by URL (for remote/mobile use)

### OpenCode Integration

OpenWork uses the official `@opencode-ai/sdk/v2/client` to:
- Connect to the OpenCode server
- List/create sessions
- Send prompts
- Subscribe to SSE events (`/event` endpoint)
- Read todos and permission requests
- Manage files and search

**Important**: UI code should import from `@opencode-ai/sdk/v2/client` to avoid Node-only server code.

### Key SDK Methods

- **Health**: `client.global.health()`
- **Sessions**: `client.session.create()`, `client.session.list()`, `client.session.prompt()`, `client.session.abort()`
- **Events**: `client.event.subscribe()` - Real-time SSE streaming
- **Permissions**: `client.permission.reply({ requestID, reply })` where reply is `once` | `always` | `reject`
- **Files**: `client.find.text()`, `client.find.files()`, `client.file.read()`, `client.file.status()`
- **Config**: `client.config.get()`, `client.config.providers()`

### State Management

OpenWork uses SolidJS signals for reactive state. Key patterns:

- **Scoped async actions**: Each async operation gets its own `pending` signal to avoid global deadlocks
- **Fine-grained reactivity**: Prefer specific signals over shared global flags
- **Derived state**: Use `createMemo()` for computed values
- **Immutable updates**: Always create new arrays/objects instead of mutating

See `.opencode/skill/solidjs-patterns/SKILL.md` for detailed patterns.

### Pages Structure

Main pages in `packages/app/src/app/pages/`:
- `dashboard.tsx` - Main workspace view
- `session.tsx` - Active session/run view
- `templates.tsx` - Template management
- `skills.tsx` - Skill manager (install from OpenPackage)
- `plugins.tsx` - Plugin manager (reads/writes `opencode.json`)
- `mcp.tsx` - MCP server management
- `settings.tsx` - App settings
- `onboarding.tsx` - First-run setup
- `forge.tsx` - Workspace creation

### Extensibility

OpenWork exposes OpenCode's native extension systems:

1. **Skills**: Installed into `.opencode/skill/*` via `opkg install` (or `pnpm dlx opkg install`)
2. **Plugins**: Configured in `opencode.json` (project or global scope)
3. **MCP Servers**: Configured in `opencode.json` under `mcpServers`
4. **Commands**: Slash commands in `.opencode/commands/`
5. **Templates**: OpenWork-specific, stored in `.openwork/templates/` as markdown files

### Folder Picker

Uses Tauri dialog plugin. Capability permissions defined in `packages/desktop/src-tauri/capabilities/default.json`.

## Development Guidelines

### Before Making Changes

1. Review `AGENTS.md` for product goals and development guidelines
2. Review `MOTIVATIONS-PHILOSOPHY.md` for the "why" behind OpenWork and detailed architecture
3. Ensure Node.js, pnpm, Rust toolchain, and `opencode` CLI are installed

### When Editing SolidJS UI

- Consult `.opencode/skill/solidjs-patterns/SKILL.md` for reactivity patterns
- Avoid global `busy()` flags that can create deadlocks with permission prompts
- Use scoped async state for each independent action
- Don't mutate signal values in-place; create new objects/arrays

### Design Reference

The design system is defined in `packages/app/src/app/theme.ts`. OpenWork targets:
- Premium, calm, high-contrast aesthetic
- 60fps animations with springy transitions
- <100ms input-to-feedback latency
- Mobile-first interaction patterns

### PRD Conventions

New PRDs go in `packages/app/pr/<name>.md` following `.opencode/skill/prd-conventions/SKILL.md` conventions.

### Testing Before PR

Run these before opening a PR:
```bash
pnpm typecheck
pnpm test:e2e
```

## Release Process

Releases are triggered by pushing a `v*` tag (e.g., `v0.3.6`). The GitHub Actions workflow builds and publishes artifacts.

### Standard Release

1. Bump versions in sync:
   ```bash
   pnpm bump:patch  # or minor/major
   ```
   This updates:
   - `packages/app/package.json`
   - `packages/desktop/package.json`
   - `packages/desktop/src-tauri/tauri.conf.json`
   - `packages/desktop/src-tauri/Cargo.toml`

2. Commit and merge to `master`

3. Create and push tag:
   ```bash
   git tag v0.3.7
   git push origin v0.3.7
   ```

### Re-run Existing Release

```bash
gh workflow run "Release App" --repo different-ai/openwork -f tag=v0.3.7
```

## OpenCode Primitives

OpenWork is a thin layer over OpenCode's native primitives:

- **MCP**: For authenticated third-party flows (OAuth) with safe capability surfaces
- **Plugins**: For real tools with scoped permissions, reusable and testable
- **Skills**: For reliable plain-english patterns that shape behavior
- **Agents**: For tasks executed by different models with extra context
- **Commands**: `/` commands that trigger tools
- **Bash/CLI**: For advanced users only (highest risk)

## Key Principles

- **Parity**: UI actions map cleanly to OpenCode server APIs
- **Transparency**: Plans, steps, tool calls, and permissions are visible
- **Least privilege**: Only user-authorized folders + explicit approvals
- **Prompt is the workflow**: Product logic lives in prompts, rules, and skills
- **Local-first**: Runs locally by default, remote connection optional
- **Extensible**: Skills and plugins are installable modules
- **Auditable**: Show what happened, when, and why

## Troubleshooting

### Linux / Wayland (Hyprland)

If OpenWork crashes on launch with WebKitGTK errors:
```bash
WEBKIT_DISABLE_DMABUF_RENDERER=1 openwork
# or
WEBKIT_DISABLE_COMPOSITING_MODE=1 openwork
```

## Requirements

- Node.js + pnpm
- Rust toolchain: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- Tauri CLI: `cargo install tauri-cli`
- OpenCode CLI installed and available on PATH: `opencode`
