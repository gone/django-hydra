import { describe, expect, it } from "vitest";

describe("main", () => {
  it("vite hmr available in tests", () => {
    if (import.meta.hot) {
      expect(import.meta.hot).toBe(true);
    }
  });
});
