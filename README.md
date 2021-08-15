# pre-commit-hook-git-crypt

See also: https://github.com/pre-commit/pre-commit

### Using pre-commit-hook-git-crypt with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/philipsd6/pre-commit-hook-git-crypt
  rev: v1.0.1  # Use the ref you want to point at
  hooks:
    - id: check-git-crypt-status
```
### Hooks available

#### `check-git-crypt-status`
Prevent unencrypted files from being committed accidentally.
  - Limits checked files to those indicated as staged for addition by git.
  - **Note:** The hook will cause an error if you try to commit empty files. See
    [pre-commit/pre-commit#776](https://github.com/pre-commit/pre-commit/issues/776).
