# cSpell: ignore venv, childitem, autopep8, pyclean, pyright, findstr, pycache, pytest

<#
.SYNOPSIS
This script automates various development tasks for a Python project.

.DESCRIPTION
The script provides functions to set up a virtual environment, build the package, 
search for spelling errors, run tests, and repair code formatting. 
It uses PowerShell to execute these tasks and ensures that the development 
environment is properly configured and maintained.

.PARAMETER Install-Venv
Sets up a virtual environment, installs required packages, and saves the frozen requirements.

.PARAMETER Build-Package
Builds the Python package using the build module.

.PARAMETER Search-Spelling
Searches for spelling errors in the Python files using cspell-cli, 
excluding certain directories.

.PARAMETER Test
Runs a series of tests including pyclean, flake8, pyright, spelling check, and pytest.

.PARAMETER Repair-Format
Repairs the code formatting using autopep8.

.EXAMPLE
.\makefile.ps1
Runs the default target, which is the Test function.

#>

$DefaultTarget = "Test"

function Install-Venv() {
	Remove-Item venv -r
	get-childitem simple_queued_pipelines -include __pycache__ -recurse | remove-item -Force -Recurse
	py -3.13t -m venv venv
	.\venv\Scripts\Activate.ps1
	python --version
	python -c "import sys; print(sys.executable)"
	.\venv\Scripts\python.exe -m pip install --upgrade pip
	pip install -r .\requirements.txt
	pip freeze > frozen_requirements.txt
}

function Build-Package() {
	py -m build
}	

function Search-Spelling() {
	& "cspell-cli" "simple_queued_pipelines/**/*.py" `
		"--no-progress" "--fail-fast" `
		"--exclude" "__pycache__" `
		"--exclude" ".git" `
		"--exclude" "venv" 
}

function Test() {
	.\venv\Scripts\Activate.ps1
	Clear-Host
	if ($?) { pyclean simple_queued_pipelines }
	if ($?) { flake8 simple_queued_pipelines }
	if ($?) { pyright simple_queued_pipelines }
	if ($?) { Search-Spelling }
	if ($?) { python -m pytest simple_queued_pipelines }
}

function Repair-Format() {
	.\venv\Scripts\Activate.ps1
	autopep8 --in-place --recursive simple_queued_pipelines
}

if ($args.Length -eq 0) {
	& $DefaultTarget
}
else {
	& $args[0]
}
