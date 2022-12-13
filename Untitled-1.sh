#!/bin/bash
export SINCE=2022-01-01


git log --pretty="%H" --author="Lucas Vianna" | while read commit_hash; do git show --oneline --name-only $commit_hash | tail -n+2; done | sort | uniq
