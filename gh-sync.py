#!/usr/bin/env python3
"""Sync Connection Mapper improvements to GitHub Issues. Run with --create to push."""
import argparse, json, os, sys
from pathlib import Path

try:
    from github import Github
    from dotenv import load_dotenv
except ImportError:
    print("Run: pip install PyGithub python-dotenv"); sys.exit(1)

load_dotenv(Path("~/memory-agent/.env").expanduser())
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO  = os.getenv("GITHUB_REPO", "yangxiang5136/digital-me")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="connections/system-improvements.json")
    parser.add_argument("--create", action="store_true")
    args = parser.parse_args()

    data = json.loads(Path(args.file).read_text())
    improvements = data if isinstance(data, list) else data.get("system_improvements", [])

    if not args.create:
        print(f"[DRY RUN] {len(improvements)} improvements found:")
        for i, imp in enumerate(improvements, 1):
            print(f"  {i}. {imp.get('title', imp.get('summary', '?'))}")
        return

    repo = Github(GITHUB_TOKEN).get_repo(GITHUB_REPO)
    existing = {i.title.lower() for i in repo.get_issues(state="open")}
    created = 0
    for imp in improvements:
        title = imp.get("title", imp.get("summary", "Untitled"))
        if title.lower() in existing:
            print(f"  [SKIP] {title}"); continue
        repo.create_issue(title=title, labels=["auto-detected"],
            body=f"Auto-created by gh-sync.py\n\n{imp.get('description','')}")
        print(f"  [CREATE] {title}"); created += 1
    print(f"Done. Created {created} issues.")

if __name__ == "__main__":
    main()
