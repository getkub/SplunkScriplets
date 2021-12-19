```
myproj="env"
python3 -m venv ${myproj}
source ${myproj}/bin/activate
```


### Ensure gitignore is kept up-to-date
```
git_ignore_file=".gitignore"
echo "${myproj}" >> ${git_ignore_file}
echo ".vscode" >> ${git_ignore_file}
echo ".DS_Store" >> ${git_ignore_file}
```

### Installing software and Freezing Requirements
```
pip install sqlalchemy
pip freeze > requirements.txt
python3
import sqlalchemy
sqlalchemy.__version__
```

