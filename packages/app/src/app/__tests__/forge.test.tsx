import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@solidjs/testing-library";

import ForgeView from "../pages/forge";

vi.mock("../lib/forge", () => ({
  checkForgeHealth: () => Promise.resolve(true),
  generateSpec: () => Promise.resolve({
    project_name: "Test",
    requirement: { summary: "Summary", description: "Description" },
    tasks: [],
  }),
}));

describe("ForgeView", () => {
  it("renders headings and connected status", async () => {
    render(() => <ForgeView />);
    expect(screen.getByText("Enterprise Forge")).toBeTruthy();
    expect(screen.getByText("OpenSpec Contract")).toBeTruthy();
    expect(await screen.findByText("Connected")).toBeTruthy();
  });
});
