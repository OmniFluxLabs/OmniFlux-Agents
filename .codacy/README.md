Codacy CLI troubleshooting
===========================

If you see errors like "env: can't execute 'bash\r': No such file or directory" when the Codacy CLI runs under WSL, follow these steps locally to normalize line endings and make the CLI script executable:

1. Ensure .gitattributes is present (this repo includes one which forces LF for shell scripts).

2. Normalize line endings in your working tree and recommit the script:

```powershell
# Re-normalize all files according to .gitattributes
git add --renormalize .
git commit -m "Normalize line endings (LF) for shell scripts"

# Ensure the script is executable in the index
git update-index --chmod=+x .codacy/cli.sh
git commit -m "Make .codacy/cli.sh executable" || echo "No changes to executable bit"
```

3. If you're using WSL and files are mounted from Windows, ensure WSL sees LF endings by cloning the repo inside WSL (recommended):

```bash
# In WSL
cd ~
git clone /mnt/c/Users/YourUser/path/to/repo
cd StayUpAgents
./.codacy/cli.sh init --provider gh --organization oO --repository figma-mcp-write-server
```

If you cannot re-clone in WSL, running the renormalize steps above from PowerShell and then restarting WSL may help.

If you still see the issue after these steps, please share the exact error and the output of `file -b --mime .codacy/cli.sh` from WSL and `git ls-files --eol .codacy/cli.sh` from PowerShell so we can debug further.

PR-ready: normalized `.codacy/cli.sh` LF endings — 2025-10-17

PR placeholder: branch prepared for PR creation (2025-10-17T18:50:00Z)
