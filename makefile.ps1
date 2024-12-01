# cSpell: ignore autopep8, childitem, findstr, isort, pycache, pyclean, pyright, pytest, venv autopep8, childitem, findstr, pycache, pyclean, pyright, pytest, venv

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
$SrcFolderName = "simple_queued_pipelines"
$PythonVersion = "3.13t"

function Build-Package() {
	py -m build
}

function Enable-Venv() {
	.\venv\Scripts\Activate.ps1
}

function Install-Venv() {
	Remove-Item venv -r
	get-childitem $SrcFolderName -include __pycache__ -recurse | remove-item -Force -Recurse
	py "-${PythonVersion}" -m venv venv
	Enable-Venv
	python --version
	python -c "import sys; print(sys.executable)"
	.\venv\Scripts\python.exe -m pip install --upgrade pip
	pip install -r .\requirements.txt
	pip freeze > requirements_frozen.txt
}

function Repair-Format() {
	Enable-Venv
	isort $SrcFolderName
	autopep8 --in-place --recursive $SrcFolderName
}

function Search-Spelling() {
	& "cspell-cli" "${SrcFolderName}/**/*.py" `
		"--no-progress" "--fail-fast" `
		"--exclude" "__pycache__" `
		"--exclude" ".git" `
		"--exclude" "venv" 
}

function Test() {
	Enable-Venv
	Clear-Host
	if ($?) { pyclean $SrcFolderName }
	if ($?) { flake8 $SrcFolderName }
	if ($?) { isort --check-only $SrcFolderName }
	if ($?) { pyright $SrcFolderName }
	if ($?) { Search-Spelling }
	if ($?) { python -m pytest $SrcFolderName }
}


if ($args.Length -eq 0) {
	& $DefaultTarget
}
else {
	& $args[0]
}
