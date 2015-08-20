This is a python-based agent that automatically stops and starts the docker containers, in order to simulate component failures. The main process can be configured with different algorithms to select the contains to stop/start.

Install and Launch
==================

Environment
-----------

- Docker
- Python 2.7.x
- Required libraries for the main program
  * pyYAML
  * plumbum
- Required libraries for extension algorithms so far
  * numpy

Python libraries can be install through 

'''shell
(sudo) pip install -r requirements.txt
'''

Activate the monkey
-------------------

'''shell
(sudo) python docker-monkey.py [some-config.yaml]
'''

The config file is optional, and if is not provided, the default 'config.yaml' file in the same directory will be used.


