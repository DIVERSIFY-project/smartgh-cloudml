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

``` bash
(sudo) pip install -r requirements.txt
```

Activate the monkey
-------------------

``` bash
(sudo) python docker-monkey.py [path/to/config]
```

The config file is optional, and if is not provided, the default 'conf.yaml' file in the same directory will be used.

Logs
---------

Log files can be found in ./logs/configname-timestamp.log, which currently records the running and stopped containers in each cycle.

Configuration
================

The agent can be configured in different perspectives, such as the interval between cycles, the failure model, the recovery model, etc. A configuration file writen in YAML is mandatory to run the agent. 

A simplest configuration can be the follows:

``` yaml
interval : 5 
failure :    
  module: basic_algos
  function : random_select
  reserve_first_arg : True
  number: 1
recovery : 
  module : basic_algos
  function : by_age
  reserve_first_arg: True
  lifespan : 3
```

The configuration is a dictionary (or a "map" as in Java) written in YAML. The first item (i.e., key-value pair) ```interval``` defines the length of each cycle, in seconds. The following two items, ```failure``` and ```recover``` defines two functions used by the main agent to select the containers to fail and to recovery, respectively. 

Each function is defined by a dictionary. In each dictionary, three items are reserved, i.e.,  ```module```,  ```function```, and ```reserve_first_arg```. The first two items defines where to find the function, and of course the module should be reachable from the current PYTHONPATH. If ```reserve_first_arg``` is true, then the first argument of this function will be fed by the agent, or any other code that call this function, and thus it is not necessary (nor allowed) to assign a value to the first argument. For each of the other arguments, we need to assign it a value, as an item in the function-defining dictionary. 

Going back to the example, the ```failure``` function is ```random_select```, defined in the module [basic_algos](https://github.com/DIVERSIFY-project/smartgh-cloudml/blob/master/monkey/basic_algos.py). The module contains some predefined functions. The ```random_select``` function is defined as:
``` python
def random_select(samples, number):
```
The first argument is the containers, and since it is reserved, we do not need to provide any value. The second argument is the number of containers to select each time, and set it to be 1 in the configuration. The monkey will randomly select one container and stop it in each cycle.

The recovery function is also one defined in ```basic_algos```, and it selects all the containers that has been stopped for 3 or more cycles, and re-start them. Here ''3'' is the number we provide for the argument ```lifespan```.
