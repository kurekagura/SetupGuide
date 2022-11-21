# Where should I use "conda command"?
Since there are packages that need to be built, the following console is recommended. Select the appropriate version.

- x64 Native Tools Command Prompt for VS 2017
- x64 Native Tools Command Prompt for VS 2019
- x64 Native Tools Command Prompt for VS 2022

# "conda create" for the experiment
Find the python version you want to use.
```
conda search python | findstr 3.7.
```
Once you have decided on a specific python version, start creating your venv. Several package versions are automatically determined depending on the python version, and these versions can be listed (It may be a rare case).
```
conda create -n tmpenv python=3.7.15 -y
conda create -n tmpenv python=3.7.15 setuptools=65.5.0 pip=22.2.2 -y
```
for example, the following packages will be installed along with python:
 - pip, setuptools, wheel, openssl, and some things.



Activate "tmpenv" and install the packages you need. You will use "conda install" and "pip install".
```
conda activate tmpenv

(tmpenv)>conda install hoge
(tmpenv)>pip install fuga
(...)
```

You will clone your target from git, install it and see how it works. In "mytemp", try and make dependencies with other packages.
```
git clone <the-target>
# Suppose "the_target" folder was created.
cd the_target
pip install -v -e .

# Other dependent packages may also be installed as well. Let's see.
pip list
```
You may want to change the version, although this is the domain of git, not Anaconda.
```
git tag --column
git checkout tags/xxx
git log -n 1

# Reisntall
pip install -v -e .
```

# "conda env export > env.yml"
Export your virtual environment "mytemp" to a. yml file (
You decide the file name.)

```
conda env export -n tmpenv > conda_tmpenv.yml
```
or
`(tmpenv)>conda env export > conda_tmpenv.yml`

<ins>I also output a "conda list" for later comparison.</ins>

```
conda list -n tmpenv > condalist_tmpenv.txt
```
or `(tmpenv)>conda list > condalist_tmpenv.txt`

# "conda env create -f env.yml"
First, I'll show you the restore command.  
I recommend that you specify the name of the environment to restore to (--name option).
```
conda env create -f conda_tmpenv.yml -n newenv
```

## Confirmation of identity
```
conda list -n newenv > condalist_newenv.txt
kdiff3 condalist_tmpenv.txt condalist_newenv.txt
```

<ins>However, this may fail, so you will need to modify the yml file yourself, the points of which are described in the next section.</ins>

Even if the creation is interrupted, "tmpenv-1" may have been created. If it is not necessary for your investigation, let's delete it.
```
conda remove -n myenv --all -y
```

# "conda rename"
You can change the name of the completed venv to official one.
```
conda rename -n newenv finalname
```
`conda rename` needed to be entered from the (base) in "Anaconda Prompt". Otherwise, you might get an error.

# Why do you need to edit "env. yml"?

<ins>Delete the last line of the output file (prefix: physical path of virtual environment) like this:</ins>
```
prefix: c:\Anaconda3\envs\tmpenv
```

## Around conda
As you can see by comparing the original env with the restored env (use `conda list`), there are cases where the same package version is installed from a different channel, and this difference can cause problems.

<ins>This is because the channel is not specified for each package</ins>, even though multiple channels are used.

For example:
```
channels:
  - conda-forge
  - defaults
```
```
conda list
--- Original env
# Name                    Version                   Build  Channel
blas                      1.0                         mkl

--- Restored env
blas                      1.0                         mkl conda-forge
```
The appropriate channel can be specified on the package in .yaml.
```
  - blas=1.0=mkl
        ↓
  - defaults::blas=1.0=mkl
```

## About pip
Any options on "pip install" are not exported in .yaml.

For example:
```
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```
The output into yml just looks like this:
```
  - pip:
    (...)
    - torch==1.13.0+cu117
    - torchaudio==0.13.0+cu117
    - torchvision==0.14.0+cu117
    (...)
```
So you must manually add the following:
```
  - pip:
    - --extra-index-url https://download.pytorch.org/whl/cu117
    (...)
    - torch==1.13.0+cu117
    - torchaudio==0.13.0+cu117
    - torchvision==0.14.0+cu117
    (...)
```
Other options are summarized in the next sections.

# pip install options

## --extra-index-url
```
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```
```
  - pip:
    - --extra-index-url https://download.pytorch.org/whl/cu117
```
## --find-links
```
pip install mmcv-full==1.7.0 -f https://download.openmmlab.com/mmcv/dist/cu117/torch1.13/index.html
```
```
  - pip:
    - --find-links https://download.openmmlab.com/mmcv/dist/cu117/torch1.13/index.html
```
## pip install "git+https://..."

### e.x.) philferriere/cocoapi
```
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"
```

```
Delete
    - pycocotools==2.0
Insert
    - git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI
```
->`ModuleNotFoundError: No module named 'numpy'`

This is not a radical solution, but use "conda install" to install cython and numpy. ([conda_tmpenv2.yml](./conda_tmpenv2.yml))

The pycocotools installation requires a cyton. Since the order cannot be maintained by `pip install`, the cyton must be installed by `conda install (in .yaml)` beforehand.

# TIPS
It is recommended that you create an temporary working directory (e.g., `conda-sandbox`) to perform these tasks. You will need a crash build until you have a "clean.yml". To get a "clean.yml", you may need to go through a bit of trial and error.

`pip install .` may involve the installation of multiple dependent packages. If you want to exclude those packages from yml and create a "clean.yml", you need to reserve "clean.yml" just before running `pip install .`.

* If you prefer editable mode, use `pip install -e .`.

For example:
```
git clone <url>/target-app
cd target-app

# Just before here to get "clean.yaml" : "conda env export> tmpenv.yml"
pip install .
# some dependencies may be installed. The yml output here is contaminated.
# But only at this stage can you validate the application
```
Or, if you get the following pip install log, make a note of the installed packages. Later, uninstall what you don't need in "clean.yml".

```
pip install .
(...)
Successfully installed cycler-0.11.0 fonttools-4.38.0 kiwisolver-1.4.4 matplotlib-3.5.3 mmdet-2.23.0 pycocotools-2.0.6 terminaltables-3.1.10

# Validation of installed packages, etc.

pip uninstall cycler fonttools kiwisolver matplotlib mmdet pycocotools terminaltables
```

# Examples
- [conda_tmpenv.yml](./conda_tmpenv.yml)
- [conda_tmpenv2.yml](./conda_tmpenv2.yml)
