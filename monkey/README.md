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

First example
---------

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

The recovery function is also one defined in ```basic_algos```, and it selects all the containers that has been stopped for 3 or more cycles, and re-start them. Here ''3'' is the number we provide for the argument ```lifespan```. The physical meaning of this recovery function is simple: it simulates a situation where every container is able to recover itself after it fails, but this recovery process lasts for 3 cycles time.

Second example
-----------

The first example is too simple. The failure model does not make sense statistically. So we make the second example (with only the failure part), which still randomly selects some containers to fail, but the number of containers to select is randomly generated following the poisson distribution.

``` yaml
failure :
  module: basic_algos
  function : random_select
  reserve_first_arg : True
  number:
    module: numpy.random
    function : poisson
    lam : 0.8
```

The main ```failure``` function is the same as before, but its parameter is no long a simple value, but another function which is defined by a dictionary. This is a function defined by numpy (which means that the numpy package need to be installed or included in the PYTHONPATH), which generates a random poisson-distributed integer with a shape value 0.8. 

The meaning of this failure function is that, we expect in average 0.8 containers to fail in each cycle. The failure of containers occurs independenly with each other, and does not directly depends on how long it has been running. The funciton works well when there are a large number of containers and the number does not vary a lot as time goes on. Otherwise, we need a slightly different ```lam``` value which is dependent to the number of currently alive containers.

``` yaml
failure :
  module: basic_algos
  function : random_select
  reserve_first_arg : True
  number:
    module: numpy.random
    function : poisson
    lam : (0.05 * len(samples))
```

Here we used yet another different way to assign a value to the ```lam``` parameter: instead of a direct value or a function defined as a dictionary, we write a python expresson surrounded by "()". The variable ```samples``` is the name of the first parameter for the failure function. Now the meaning is that in each cycle, 5% of the alive containers might fail.

Third example
============

In this example, we would like to fail containers based on their ages. The same function ```basic_algos.by_age``` in the first example is still useful here, but instead of a flat lifespan of 3, we will give each container a random life span when it is born, and when that time comes, the container will be selected to stop.

``` python
failure :
  module: basic_algos
  function : by_age
  reserve_first_arg : True
  lifespan :
    module : basic_algos
    function : two_param_weibull
    shape : 1.5
    scale : 20
 ```

Here we use a two-parameter weibull generator, which we wrote on the base of the first parameter ```numpy.random.weibull```. The ```shape``` parameter determines whether a component will failure densely in the beginning (```shape < 1```) or when it is getting old ```shape>1```). The ```scale``` is also called the "charasteristic life", and by setting it to be 20, we mean that approximately 63% of the containers will die before they reach the age 20, and this is irrelavant to the shape.

