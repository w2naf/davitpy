#!/bin/bash

# Python install script for Ubuntu
#	installs all pre-requisite software to run DaViT-py
#	tested on Ubuntu 12.04

#ver=2.7
#yum -y install -y python$ver
#yum -y install -d python-dev

yum -y install -y python-pip
yum -y install -y python-zmq
yum -y install -y python-imaging
yum -y install -y mpich2
yum -y install -y gcc-gfortran

#yum -y install -y libhdf5-serial-dev
#yum -y install -y python-matplotlib
#pip install --upgrade matplotlib
#yum -y install -y python-mpltoolkits.basemap
pip install --upgrade ipython
yum -y install -y ipython-notebook
pip install --upgrade numpy
pip install scipy
pip install --upgrade basemap
pip install --upgrade h5py
pip install --upgrade tornado
pip install --upgrade paramiko
pip install --upgrade pymongo
pip install --upgrade mechanize
pip install --upgrade jinja2
pip install --upgrade ecdsa
pip install --upgrade pandas
yum -y install -y libnetcdf-dev
pip install --upgrade netcdf4



dir=$(pwd)
echo "source $dir/../profile.bash" >> ~/.bashrc
