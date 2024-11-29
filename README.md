# Simple Queued Pipelines
Simple package to create thread-backed queued pipelines in Python

## Concepts

### Sink

This class abstracts a pool of threads consuming a queue.

### Pipe

This class abstracts a pool of threads consuming one queue and publishing to another queue.

### GeneratingSource

This class abstracts a pool of threads each consuming a generator (a function that yields) and publishes the iterated values to a queue.

### Execution Graphs

These are orchestrations connecting sources, pipes, and sinks to run until exhausted.
The function `execute_single_channel_linear_execution_graph_with_four_stages` has a source, 2 pipes, and a sink.  

## Helpful Notes for Developers

<!-- cSpell: ignore venv, childitem, autopep8, pyclean, pyright, findstr, pycache, pytest -->

### Installing Python on Windows
Use Microsoft Store or [download link](https://www.python.org/downloads/release/python-397/)
- Screen 1
    - Customize
- Optional Features (only check)
    - pip
    - py launcher
- Advanced Options (only check)
    - Precompile standard library
- Disable MAX_PATH

Go into Windows Terminal
```ps1
py -0  # to see what version is default
python --version # to double confirm

rm venv -r # to remove the venv folder
get-childitem simple_queued_pipelines -include __pycache__ -recurse | remove-item -Force -Recurse
py -3.13t -m venv venv
.\venv\Scripts\Activate.ps1
python --version
python -c "import sys; print(sys.executable)"
.\venv\Scripts\python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt
pip freeze > frozen_requirements.txt
py -m build
```
Then Close and reopen VSCode

### Handy command lines

```
. .\venv\Scripts\Activate.ps1
flake8 simple_queued_pipelines
.\venv\Scripts\Activate.ps1 ; clear ; if ($?) { pyclean simple_queued_pipelines } ; if ($?) { flake8 simple_queued_pipelines } ; if ($?) { pyright simple_queued_pipelines } ; if ($?) { python -m pytest simple_queued_pipelines }
autopep8 --recursive --diff simple_queued_pipelines | findstr /i /c:'--- original/'
autopep8 --recursive  --in-place simple_queued_pipelines
& "cspell-cli" "simple_queued_pipelines/**/*.py" "--no-summary" "--no-progress" "--exclude" "__pycache__" "--exclude" ".git" "--exclude" "venv" "--fail-fast"
```
