import os
import sys
import requests

MAX_DIFF_CHARS = 100_000  # keep well within context, avoid huge token cost


def get_diff():
    with open("pr.diff", "r") as f:
        diff = f.read()
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n\n[diff truncated due to size]"
    return diff


def build_prompt(diff):
    return f"""You are an experienced software engineer performing a pull request code review.

Review the following diff. Focus on:
1. Bugs and logic errors
2. Security issues (injection, auth, secrets, unsafe deserialization, etc.)
3. Code quality, readability, and maintainability
4. Missing edge cases or error handling

Be specific — reference file names and line context from the diff. Skip nitpicks unless they matter. If something is fine, don't invent issues.

Format your response as GitHub-flavored markdown with these sections:
## Summary
## Issues Found
## Suggestions
## Verdict (Approve / Request Changes / Comment)

Diff:


"""


def review_with_github_models(diff):
    token = os.environ["GITHUB_TOKEN"]
    url = "https://models.github.ai/inference/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": build_prompt(diff)}],
        "max_tokens": 2000,
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def post_comment(body):
    repo = os.environ["REPO"]
    pr_number = os.environ["PR_NUMBER"]
    token = os.environ["GITHUB_TOKEN"]

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    resp = requests.post(url, headers=headers, json={"body": body})
    resp.raise_for_status()


def main():
    diff = get_diff()
    if not diff.strip():
        post_comment("**AI PR Review:** No changes detected in diff.")
        return

    try:
        review = review_with_github_models(diff)
    except Exception as e:
        print(f"Error calling GitHub Models API: {e}", file=sys.stderr)
        post_comment(f"**AI PR Review failed:** {e}")
        sys.exit(1)

    comment = f"## 🤖 AI PR Review\n\n{review}\n\n---\n*Generated automatically via GitHub Models.*"
    post_comment(comment)


if __name__ == "__main__":
    main()