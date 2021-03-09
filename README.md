# visiontoolkit5

opensource industrial framework: computer vision module

# Development environment setup

## Linux environment

```
pyenv virtualenv 3.7.9 venv

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate venv

pip install -r requirements.txt
```

## Windows environment

```
pip3 install virtualenv 

virtualenv venv 

venv\Scripts\activate
```

# Program execution

```
python app.py
```