#!/usr/bin/env node
const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function repoRoot() {
    return path.resolve(__dirname, "..");
}

function writeFallback(outputPath) {
    const content = `# JavaScript API

This page will contain auto-generated JavaScript API documentation.

## Current Status

The JavaScript source files exist but don't yet have JSDoc comments. To generate documentation:

1. Add JSDoc comments to JavaScript files
2. Run ./scripts/generate-jsdocs.sh or run the pre-commit hook

## Source Files

- octoprint_temp_eta/static/js/temp_eta.js

`;
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, content, "utf8");
}

function normalize(text) {
    // remove trailing whitespace on lines
    text = text.replace(/[ \t]+$/gm, "");
    // ensure exactly one trailing newline
    text = text.replace(/\n+$/s, "\n");
    return text;
}

function main() {
    const root = repoRoot();
    const jsSrc = path.join(root, "octoprint_temp_eta", "static", "js");
    const docsApi = path.join(root, "docs", "api");
    const output = path.join(docsApi, "javascript.md");

    // check for JS files
    const hasJs = fs.existsSync(jsSrc) && fs.readdirSync(jsSrc).some(f => f.endsWith('.js'));
    if (!hasJs) {
        console.warn("Warning: No JavaScript files found");
        writeFallback(output);
        console.log(`Generated ${output}`);
        return 0;
    }

    // run jsdoc2md
    try {
        const args = ["--configure", "jsdoc.json", "octoprint_temp_eta/static/js/**/*.js"];
        const res = spawnSync("jsdoc2md", args, { cwd: root, encoding: "utf8" });
        if (res.error) {
            console.error("jsdoc2md invocation failed:", res.error.message);
            return 2;
        }
        if (res.status !== 0) {
            console.error(res.stderr || "jsdoc2md failed");
            return res.status || 1;
        }

        const normalized = normalize(res.stdout || "");
        fs.mkdirSync(docsApi, { recursive: true });
        fs.writeFileSync(output, normalized, "utf8");
        console.log(`Generated ${output}`);
        return 0;
    } catch (e) {
        console.error("JSDoc generation failed:", e && e.message ? e.message : e);
        return 1;
    }
}

process.exitCode = main();
