#!/bin/bash

install_pyenv() {
    # Check if git installed
    git --version 2>&1 >/dev/null
    
    if [ $? -ne 0 ];
    then
        echo "Installing git..."
        sudo apt install git
    fi
    
    PYENV_DIR=$HOME/.pyenv
    
    if [ -d $PYENV_DIR ];
    then
        echo "pyenv already exists, skip installing pyenv!"
    else
        # Install pyenv and pyenv-virtualenv
        echo "Installing pyenv and pyenv-virtualenv"
        git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
        git clone https://github.com/pyenv/pyenv-virtualenv.git $HOME/.pyenv/plugins/pyenv-virtualenv
    fi
    
    # Set up pyenv paths
    SHELL_CONFIG_FILE="$HOME/.bashrc"
    PYENV_CMD_TITLE="# pyenv"
    PYENV_CMD1="export PYENV_ROOT=\"\$HOME/.pyenv\""
    PYENV_CMD2="command -v pyenv >/dev/null || export PATH=\"\$PYENV_ROOT/bin:\$PATH\""
    PYENV_CMD3="eval \"\$(pyenv init -)\""
    
    if ! grep -Fxq "${PYENV_CMD_TITLE}" ${SHELL_CONFIG_FILE}
    then
        echo "Setting up pyenv configuration in ${SHELL_CONFIG_FILE}"
        echo ${PYENV_CMD_TITLE} >> ${SHELL_CONFIG_FILE}
        echo ${PYENV_CMD1} >> ${SHELL_CONFIG_FILE}
        echo ${PYENV_CMD2} >> ${SHELL_CONFIG_FILE}
        echo ${PYENV_CMD3} >> ${SHELL_CONFIG_FILE}
    else
        echo "pyenv configuration exists"
    fi
}

set_up_env() {
    ENV_NAME="py310"
    PYTHON_VERSION=3.10.12

    # Check if pyenv exists
    pyenv --version 2>&1 >/dev/null

    if [ $? -ne 0 ];
    then
	echo "pyenv command not found!"
	exit 1
    fi

    echo "setting up env ${ENV_NAME} with Python ${PYTHON_VERSION}"
    pyenv install ${PYTHON_VERSION}
    pyenv virtualenv ${PYTHON_VERSION} ${ENV_NAME}
}

usage() {
    echo "Usage: $0 <-i|-s>" 1>&2;
    echo "-i: install pyenv"
    echo "-s: set up pyenv environment"
}

no_args=1
while getopts ":is" flag
do
    case "${flag}" in
        i) install_pyenv;;
        s) set_up_env;;
	*) usage;;
    esac
    no_args=0
done

if [ $no_args -eq 1 ];
then
    usage
fi
