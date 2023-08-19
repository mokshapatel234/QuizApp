# This script sets up the virtual environment to be used in
# the bitbucket pipeline when constructing the zip file to
# be deployed to AWS instances
python3 --version

echo "Installing venv for python3"
sudo apt-get install -y python3-venv

VENV_DIRECTORY=env
echo "Setting up virtual environment at $VENV_DIRECTORY"
sudo python3 -m venv $VENV_DIRECTORY

echo "Activating the virtual environment"
source $VENV_DIRECTORY/bin/activate

echo "Checking which pip3 and python3 is being used"
which python3
which pip3

# echo "Upgrading pip in the virtual environment"
python3 -m pip install --upgrade --force pip

echo "Installing dependencies in the virtual environment"
pip3 install -r requirements.txt

echo "Deactivating the virtual environment"
deactivate