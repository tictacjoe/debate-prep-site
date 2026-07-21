const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

function extractFunction(source, name) {
  const startMarker = `/* ${name}:start */`;
  const endMarker = `/* ${name}:end */`;
  const start = source.indexOf(startMarker);
  const end = source.indexOf(endMarker);
  if (start === -1 || end === -1) {
    throw new Error(`Markers for ${name} not found in index.html`);
  }
  return source.slice(start + startMarker.length, end);
}

const indexHtmlPath = path.join(__dirname, "..", "index.html");
const source = fs.readFileSync(indexHtmlPath, "utf8");
const functionSource = extractFunction(source, "summary-line");
const summaryLineHtml = (0, eval)(`${functionSource}\nsummaryLineHtml;`);

test("returns empty string when summary is undefined", () => {
  assert.equal(summaryLineHtml(undefined), "");
});

test("returns empty string when summary is an empty string", () => {
  assert.equal(summaryLineHtml(""), "");
});

test("wraps a present summary in a bold field-summary paragraph", () => {
  assert.equal(
    summaryLineHtml("High confidence on the documented facts."),
    '<p class="field-summary">High confidence on the documented facts.</p>'
  );
});
