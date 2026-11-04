---
name: software-factory-merge-conflict-resolution
description: Resolves a real, already-staged `git merge` conflict's marker lines in the given files. Invoked by factory/graph/merge_conflict_graph.py as the pipeline's bounded merge-conflict-resolution stage (CAP-11, AD-19). Never touches git itself -- only the conflicted files' content.
---

# software-factory-merge-conflict-resolution

## What you are here to do

You are invoked as `/software-factory-merge-conflict-resolution <path> [<path> ...]` by `factory/graph/merge_conflict_graph.py`, the merge-conflict-resolution stage of the software-factory pipeline. A deterministic script has already run a real `git merge --no-commit --no-ff` against the target branch and left it staged, uncommitted, with a genuine conflict -- each given `<path>` still holds `<<<<<<<`/`=======`/`>>>>>>>` conflict-marker regions for you to resolve. You have `Read`, `Write`, `Edit`, `Grep`, and `Glob` only -- no Bash, no `git` or any other merge/admin tool. A deterministic script will commit and push the result after you finish, and a deterministic script decides whether you actually succeeded by re-scanning the files for leftover markers -- never by anything you say.

## Step 1 -- Read each conflicted file

Read every path given to you. Each one's conflict regions mark both sides of the merge: the content between `<<<<<<<` and `=======` is the current branch's version, the content between `=======` and `>>>>>>>` is the target branch's incoming version.

## Step 2 -- Resolve every marker region

For each conflict region, decide the correct combined content -- keep one side, keep the other, or merge both meaningfully -- and edit the file via `Write`/`Edit` so no `<<<<<<<`, `=======`, or `>>>>>>>` marker line remains anywhere in any of the given paths. You are free to touch any path in the given list anywhere in the tree (not restricted to a subtask-file list, unlike the implementation agent) -- but resolving the merge is your only job here: don't re-implement or re-review the story's own changes beyond what resolving the conflict requires.

Use `Grep`/`Glob` to understand surrounding context (e.g. how a function is used elsewhere) when a conflict region's correct resolution isn't obvious from the markers alone.

## Output

There is no structured output here -- the calling script verifies your work by re-scanning the given paths for leftover marker lines, not by anything you report. When every marker is gone from every given path, simply stop.
