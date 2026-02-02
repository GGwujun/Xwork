import { For, Show, createMemo, createSignal, createEffect } from "solid-js";

import type { SkillCard } from "../types";

import Button from "../components/button";
import { FolderOpen, Package, Upload } from "lucide-solid";
import { currentLocale, t } from "../../i18n";

export type SkillsViewProps = {
  busy: boolean;
  mode: "host" | "client" | null;
  refreshSkills: (options?: { force?: boolean }) => void;
  skills: SkillCard[];
  skillsStatus: string | null;
  importLocalSkill: () => void;
  installSkillCreator: () => void;
  revealSkillsFolder: () => void;
  uninstallSkill: (name: string) => void;
};

export default function SkillsView(props: SkillsViewProps) {
  // Translation helper that uses current language from i18n
  const translate = (key: string) => t(key, currentLocale());

  const skillCreatorInstalled = createMemo(() =>
    props.skills.some((skill) => skill.name === "skill-creator")
  );

  const [uninstallTarget, setUninstallTarget] = createSignal<SkillCard | null>(null);
  const uninstallOpen = createMemo(() => uninstallTarget() != null);

  const [searchQuery, setSearchQuery] = createSignal("");
  const [searchTags, setSearchTags] = createSignal("");
  const [searchResults, setSearchResults] = createSignal<
    { skill: SkillCard; score: number }[]
  >([]);
  const [searching, setSearching] = createSignal(false);
  const [selectedSkill, setSelectedSkill] = createSignal<SkillCard | null>(null);
  const [stats, setStats] = createSignal({
    total: 0,
    lastRefresh: "",
    lastQuery: "",
  });

  createEffect(() => {
    setStats((current) => ({
      ...current,
      total: props.skills.length,
    }));
  });

  const mapSkillCard = (input: any): SkillCard => ({
    name: input?.name ?? "",
    description: input?.description ?? "",
    path: input?.file_path ?? input?.path ?? "",
    tags: Array.isArray(input?.tags) ? input.tags : [],
  });

  const fetchSearchResults = async () => {
    if (!searchQuery().trim()) {
      setSearchResults([]);
      return;
    }
    setSearching(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/skills/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: searchQuery().trim(),
          tags: searchTags()
            .split(",")
            .map((tag) => tag.trim())
            .filter(Boolean),
          top_k: 5,
        }),
      });
      if (!response.ok) {
        throw new Error("Failed to search skills");
      }
      const data = await response.json();
      const results = Array.isArray(data)
        ? data.map((item) => ({
            skill: mapSkillCard(item.skill ?? item),
            score: typeof item.score === "number" ? item.score : 0,
          }))
        : [];
      setSearchResults(results);
      setStats((current) => ({
        ...current,
        lastQuery: searchQuery().trim(),
        lastRefresh: new Date().toLocaleTimeString(),
      }));
    } catch (error) {
      console.error(error);
    } finally {
      setSearching(false);
    }
  };

  return (
    <section class="space-y-8">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-12">{translate("skills.title")}</h3>
          <p class="text-sm text-gray-10 mt-1">{translate("skills.subtitle")}</p>
        </div>
        <Button variant="secondary" onClick={() => props.refreshSkills({ force: true })} disabled={props.busy}>
          {translate("skills.refresh")}
        </Button>
      </div>

      <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 overflow-hidden">
        <div class="flex flex-wrap items-center justify-between gap-3 px-5 py-4 border-b border-gray-6/60 bg-gray-2/40">
          <div>
            <div class="text-xs font-semibold text-gray-11 uppercase tracking-wider">{translate("skills.add_title")}</div>
            <div class="text-sm text-gray-10 mt-2">{translate("skills.add_description")}</div>
          </div>
          <Show when={props.mode !== "host"}>
            <div class="text-xs text-gray-10">{translate("skills.host_mode_only")}</div>
          </Show>
        </div>

        <div class="divide-y divide-gray-6/60">
          <div class="flex flex-wrap items-center justify-between gap-3 px-5 py-4">
            <div>
              <div class="text-sm font-medium text-gray-12">{translate("skills.install_skill_creator")}</div>
              <div class="text-xs text-gray-10 mt-1">{translate("skills.install_skill_creator_hint")}</div>
            </div>
            <Button
              variant={skillCreatorInstalled() ? "outline" : "secondary"}
              onClick={() => {
                if (skillCreatorInstalled()) return;
                props.installSkillCreator();
              }}
              disabled={props.busy || skillCreatorInstalled()}
            >
              <Package size={16} />
              {skillCreatorInstalled() ? translate("skills.installed_label") : translate("skills.install")}
            </Button>
          </div>

          <div class="flex flex-wrap items-center justify-between gap-3 px-5 py-4">
            <div>
              <div class="text-sm font-medium text-gray-12">{translate("skills.import_local")}</div>
              <div class="text-xs text-gray-10 mt-1">{translate("skills.import_local_hint")}</div>
            </div>
            <Button variant="secondary" onClick={props.importLocalSkill} disabled={props.busy}>
              <Upload size={16} />
              {translate("skills.import")}
            </Button>
          </div>

          <div class="flex flex-wrap items-center justify-between gap-3 px-5 py-4">
            <div>
              <div class="text-sm font-medium text-gray-12">{translate("skills.reveal_folder")}</div>
              <div class="text-xs text-gray-10 mt-1">{translate("skills.reveal_folder_hint")}</div>
            </div>
            <Button variant="secondary" onClick={props.revealSkillsFolder} disabled={props.busy}>
              <FolderOpen size={16} />
              {translate("skills.reveal_button")}
            </Button>
          </div>
        </div>

        <Show when={props.skillsStatus}>
          <div class="border-t border-gray-6/60 px-5 py-3 text-xs text-gray-11 whitespace-pre-wrap break-words">
            {props.skillsStatus}
          </div>
        </Show>
      </div>

      <div class="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
        <div>
          <div class="flex items-center justify-between mb-3">
            <div>
              <div class="text-sm font-semibold text-gray-12">{translate("skills.installed")}</div>
              <div class="text-xs text-gray-10 mt-1">{translate("skills.installed_description")}</div>
            </div>
            <div class="text-xs text-gray-10">{stats().total}</div>
          </div>

          <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 p-4 mb-4 space-y-3">
            <div class="text-xs uppercase tracking-wider text-gray-11 font-semibold">
              {translate("skills.search_title")}
            </div>
            <div class="grid gap-3 md:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]">
              <input
                value={searchQuery()}
                onInput={(event) => setSearchQuery(event.currentTarget.value)}
                placeholder={translate("skills.search_skills_placeholder")}
                class="h-10 rounded-xl bg-gray-1/40 border border-gray-6/60 px-3 text-sm text-gray-12"
              />
              <input
                value={searchTags()}
                onInput={(event) => setSearchTags(event.currentTarget.value)}
                placeholder={translate("skills.search_tags_placeholder")}
                class="h-10 rounded-xl bg-gray-1/40 border border-gray-6/60 px-3 text-sm text-gray-12"
              />
              <Button
                variant="secondary"
                onClick={fetchSearchResults}
                disabled={searching()}
              >
                {searching()
                  ? translate("skills.searching")
                  : translate("skills.search_button")}
              </Button>
            </div>
            <div class="grid gap-2 text-xs text-gray-10 md:grid-cols-3">
              <div>
                {translate("skills.stats_last_query")}: {stats().lastQuery || "-"}
              </div>
              <div>
                {translate("skills.stats_last_refresh")}: {stats().lastRefresh || "-"}
              </div>
              <div>
                {translate("skills.stats_total")}: {stats().total}
              </div>
            </div>
          </div>

          <Show
            when={props.skills.length}
            fallback={
              <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 px-5 py-6 text-sm text-zinc-500">
                {translate("skills.no_skills")}
              </div>
            }
          >
            <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 divide-y divide-gray-6/60">
              <For each={props.skills}>
                {(s) => (
                  <div class="px-5 py-4">
                    <div class="flex flex-wrap items-start justify-between gap-3">
                      <div class="space-y-2">
                        <button
                          type="button"
                          class="flex items-center gap-2"
                          onClick={() => setSelectedSkill(s)}
                        >
                          <Package size={16} class="text-gray-11" />
                          <div class="font-medium text-gray-12">{s.name}</div>
                        </button>
                        <Show when={s.description}>
                          <div class="text-sm text-gray-10">{s.description}</div>
                        </Show>
                        <div class="text-xs text-gray-7 font-mono">{s.path}</div>
                      </div>
                      <Button
                        variant="danger"
                        class="!px-3 !py-2 text-xs"
                        onClick={() => setUninstallTarget(s)}
                        disabled={props.busy}
                        title={translate("skills.uninstall")}
                      >
                        {translate("skills.uninstall")}
                      </Button>
                    </div>
                  </div>
                )}
              </For>
            </div>
          </Show>
        </div>

        <div class="space-y-4">
          <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 p-4">
            <div class="text-xs uppercase tracking-wider text-gray-11 font-semibold">
              {translate("skills.search_results_title")}
            </div>
            <Show
              when={searchResults().length}
              fallback={<div class="text-sm text-gray-10 mt-3">{translate("skills.search_empty")}</div>}
            >
              <div class="mt-3 space-y-3">
                <For each={searchResults()}>
                  {(result) => (
                    <button
                      type="button"
                      class="w-full text-left rounded-xl border border-gray-6/60 bg-gray-2/30 px-3 py-2"
                      onClick={() => setSelectedSkill(result.skill)}
                    >
                      <div class="flex items-center justify-between">
                        <div class="text-sm font-medium text-gray-12">{result.skill.name}</div>
                        <div class="text-xs text-gray-9">Score {result.score.toFixed(2)}</div>
                      </div>
                      <div class="text-xs text-gray-10 mt-1">{result.skill.description}</div>
                    </button>
                  )}
                </For>
              </div>
            </Show>
          </div>

          <div class="rounded-2xl border border-gray-6/60 bg-gray-1/40 p-4">
            <div class="text-xs uppercase tracking-wider text-gray-11 font-semibold">
              {translate("skills.preview_title")}
            </div>
            <Show
              when={selectedSkill()}
              fallback={<div class="text-sm text-gray-10 mt-3">{translate("skills.preview_empty")}</div>}
            >
              <div class="mt-3 space-y-2">
                <div class="text-sm font-semibold text-gray-12">{selectedSkill()?.name}</div>
                <div class="text-xs text-gray-10">{selectedSkill()?.description}</div>
                <div class="text-xs text-gray-7 font-mono break-all">{selectedSkill()?.path}</div>
              </div>
            </Show>
          </div>
        </div>
      </div>

      <Show when={uninstallOpen()}>
        <div class="fixed inset-0 z-50 bg-gray-1/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div class="bg-gray-2 border border-gray-6/70 w-full max-w-md rounded-2xl shadow-2xl overflow-hidden">
            <div class="p-6">
              <div class="flex items-start justify-between gap-4">
                <div>
                  <h3 class="text-lg font-semibold text-gray-12">{translate("skills.uninstall_title")}</h3>
                  <p class="text-sm text-gray-11 mt-1">
                    {translate("skills.uninstall_warning").replace("{name}", uninstallTarget()?.name ?? "")}
                  </p>
                </div>
              </div>

              <div class="mt-4 rounded-xl bg-gray-1/20 border border-gray-6 p-3 text-xs text-gray-11 font-mono break-all">
                {uninstallTarget()?.path}
              </div>

              <div class="mt-6 flex justify-end gap-2">
                <Button variant="outline" onClick={() => setUninstallTarget(null)} disabled={props.busy}>
                  {translate("common.cancel")}
                </Button>
                <Button
                  variant="danger"
                  onClick={() => {
                    const target = uninstallTarget();
                    setUninstallTarget(null);
                    if (!target) return;
                    props.uninstallSkill(target.name);
                  }}
                  disabled={props.busy}
                >
                  {translate("skills.uninstall")}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </Show>
    </section>
  );
}
