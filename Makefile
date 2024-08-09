PYTHON_VERSION := 3.11
CONDA_ENV_NAME := reportgen
ENV_FILE_NAME := reportgen_conda_env

env-save:
	@conda env export -n $(CONDA_ENV_NAME) --no-builds | grep -v "prefix" > $(ENV_FILE_NAME).yml

env-create:
	@conda env create -n $(CONDA_ENV_NAME) --file $(ENV_FILE_NAME).yml

env-remove:
	@conda env remove -n $(CONDA_ENV_NAME) --yes
