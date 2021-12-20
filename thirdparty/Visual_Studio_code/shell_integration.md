### Update to user/workspace settings.json

`ShortCut Key: Control+Shift+p`

```
{
    "workbench.colorTheme": "Default Dark+",
    "git.ignoreMissingGitWarning": true,
    "git.enabled": true,
    "git.path": "C:\\installables\\PortableGit\\bin\\git.exe",
    "terminal.integrated.shell.windows": "C:\\installables\\PortableGit\\bin\\bash.exe"
}
```


### Cygwin
https://stackoverflow.com/questions/46061894/vs-code-cygwin-as-integrated-terminal/48545827
```
{
    "workbench.colorTheme": "Default Dark+",
    "git.ignoreMissingGitWarning": true,
    "git.enabled": true,
    "git.path": "C:\\Program Files\\Git\\bin\\git.exe",
    "terminal.integrated.shell.windows": "C:\\Program Files\\cygwin2.8\\bin\\bash.exe",
    "terminal.integrated.env.windows": {
        "CHERE_INVOKING": "1"
      },
    // Make it a login shell
    "terminal.integrated.shellArgs.windows": [
        "-l"
    ],
    "workbench.startupEditor": "none"
}
```
