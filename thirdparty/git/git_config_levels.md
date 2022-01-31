### There are 3 levels of git config; project, global and system.

-----------------------------------------------
- project: Project configs are only available for the current project and stored in .git/config in the project's directory.
- global: Global configs are available for all projects for the current user and stored in ~/.gitconfig.
- system: System configs are available for all the users/projects and stored in /etc/gitconfig.
-----------------------------------------------

```
# Create a project specific config, you have to execute this under the project's directory.
$ git config user.name "John Local_to_project"

# Create a global config
$ git config --global user.name "John Global_for_user"

# Create a system config
$ git config --system user.name "MY_HOST_DEFAULT"
```
