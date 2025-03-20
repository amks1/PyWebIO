
1. Read `webiojs/README.md` and build the js files
2. In `./.gitignore`, remove the line `pywebio/html/js/pywebio.min.*` 
3. Update the new branch name in FMConsole `pip/constraints.txt`
4. Identify the CDN path. Eg: https://cdn.jsdelivr.net/gh/amks1/PyWebIO@amal-1.8.3-pinvalues/pywebio/html (change the branch name as required)
5. Update the CDN in fmconsole/settings/modular_apps.py