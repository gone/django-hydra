import { beforeAll, describe, expect, it } from "vitest";
import linksInit, { isCurrentPage, isExternalLink } from "../links";

const mockAnchor = (href: string) => ({ href } as HTMLAnchorElement);

describe("links", () => {
  beforeAll(() => {
    window.location.href = "https://test.com/example/";
  });
  it("isExternalLink", () => {
    // internal links
    expect(isExternalLink(mockAnchor(""))).toBe(false);
    expect(isExternalLink(mockAnchor("https://test.com/a#foo"))).toBe(false);
    expect(isExternalLink(mockAnchor("/newpage"))).toBe(false);
    expect(isExternalLink(mockAnchor("#anchor-ref"))).toBe(false);
    expect(isExternalLink(mockAnchor("?foo=bar"))).toBe(false);
    expect(isExternalLink(mockAnchor("tel:2013334444"))).toBe(false);
    expect(isExternalLink(mockAnchor("mailto:example@test.com"))).toBe(false);
    expect(isExternalLink(mockAnchor("https://test.com"))).toBe(false);

    // external links
    expect(isExternalLink(mockAnchor("https://example.com"))).toBe(true);
    expect(isExternalLink(mockAnchor("https://example.com/#anchor-ref"))).toBe(true);
    expect(isExternalLink(mockAnchor("ftp://test.com"))).toBe(true);
  });

  it("isCurrentPage", () => {
    // same page
    expect(isCurrentPage(mockAnchor("https://test.com/example/"))).toBe(true);
    expect(isCurrentPage(mockAnchor("/example/#anchor-ref"))).toBe(true);
    expect(isCurrentPage(mockAnchor("https://test.com/example/#anchor-ref"))).toBe(true);
    // diff page
    expect(isCurrentPage(mockAnchor("https://test.com"))).toBe(false); // needs trailing slash
    expect(isCurrentPage(mockAnchor("https://example.com/"))).toBe(false); // other domain
    expect(isCurrentPage(mockAnchor("https://test.com/otherpage"))).toBe(false); // other page on same domain
  });

  it("linksInit", () => {
    document.body.innerHTML = `
    <a id="active" href="/" class="active" />
    <a id="external" href="https://example.com" target="foo" />
    <a id="current" href="/example/#bar" />
    `;
    const activeLink = document.getElementById("active") as HTMLAnchorElement;
    const externalLink = document.getElementById("external") as HTMLAnchorElement;
    const currentPageLink = document.getElementById("current") as HTMLAnchorElement;

    linksInit();

    expect(activeLink.classList.contains("active")).toBe(false);
    expect(externalLink.target).toBe("_blank");
    expect(currentPageLink.classList.contains("active")).toBe(true);
    expect(currentPageLink.classList.contains("active")).toBe(true);
  });
});
