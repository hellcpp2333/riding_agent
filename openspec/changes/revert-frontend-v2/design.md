## Context

The `polish-ui-preserve-map-layout` change added `static/css/style.css` and replaced the inline `<style>` block. Reverting restores the original.

## Goals / Non-Goals

**Goals:** Restore original single-file frontend. **Non-Goals:** No backend changes.

## Decisions

Use `git restore static/index.html` and `rm -rf static/css/`. Simplest approach.
