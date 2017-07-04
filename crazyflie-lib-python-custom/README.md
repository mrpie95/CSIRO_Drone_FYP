# cflib: Crazyflie python library 

cflib is an API written in Python that is used to communicate with the Crazyflie
and Crazyflie 2.0 quadcopters. It is intended to be used by client software to
communicate with and control a Crazyflie quadcopter. 

### Linux, OSX, Windows
* Build a [virtualenv (local python environment)](https://virtualenv.pypa.io/en/latest/) with package dependencies
  * `pip install virtualenv`
  * `virtualenv venv`
  * `source venv/bin/activate`
* `pip install -r requirements.txt`
* Activate the environment: `source venv/bin/activate`
* Connect the crazyflie and run an example: `python -m examples.basiclog`
* Deactivate the virtualenv if you activated it `deactivate`

# Testing
### With docker and the toolbelt

For information and installation of the 
[toolbelt.](https://wiki.bitcraze.io/projects:dockerbuilderimage:index)
  
* Check to see if you pass tests: `tb test`
* Check to see if you pass style guidelines: `tb verify`

Note: Docker and the toolbelt is an optional way of running tests and reduces the 
work needed to maintain your python environmet. 

### Native python on Linux, OSX, Windows
* [Tox](http://tox.readthedocs.org/en/latest/) is used for native testing: `pip install tox`
* Test package in python2.7 `TOXENV=py27 tox`
* Test package in python3.4 `TOXENV=py34 tox`

Note: You must have the specific python versions on your machine or tests will fail. (ie. without specifying the TOXENV, `tox` runs tests for python2.7, 3.3, 3.4 and would require all python versions to be installed on the machine.)


## Platform notes

### Linux

#### Setting udev permissions

The following steps make it possible to use the USB Radio without being root.

```
sudo groupadd plugdev
sudo usermod -a -G plugdev <username>
```

Create a file named ```/etc/udev/rules.d/99-crazyradio.rules``` and add the
following:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev"
```

To connect Crazyflie 2.0 via usb, create a file name ```/etc/udev/rules.d/99-crazyflie.rules``` and add the following:
```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev"
```

[cfclient]: https://www.github.com/bitcraze/crazyflie-clients-python
