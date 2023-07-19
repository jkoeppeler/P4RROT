# P4RROT

Generating P4 Code for the Application Layer

## Motivation

Throughput and latency-critical applications (e.g. processing sensor data, robot control, or monitoring stock market streams) can often benefit if computations are performed close to the client. Performing these computations in the data plane can help us take it to the next level.

P4 is excellent data plane programming language, and we all love it. However, it wasn't meant to implement application-layer tasks. Thus, offloading server functionality can be challenging.

P4RROT is a code generator that helps programmers overcome certain limitations and write shorter and easier-to-read code.

## How does it work?

Code generation can greatly simplify implementing application-layer tasks if we narrow down the scope of features.

Based on a Python script and a P4 template, P4RROT generates P4 code that can be compiled to the desired target. 

## Supported targets

P4RROT is a very young project. The current code base supports BMv2,Netronome NFP and Tofino.

## Getting started

A more detailed description of P4RROT can be found in our preprint paper.

A hands-on Hello World tutorial is also available at [examples/hello-world](examples/hello-world).

## Contributing

Any kind of contribution is appreciated ranging from tutorial writing to bug fixes and implementing new features. In short, we use GitHub to host code, track issues and feature requests, as well as accept pull requests.

Read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## Discalimer

The library is released under MIT license but please note that some of the tests, examples and templates might have different licensing.


## Automated Tests
The repository currently includes a docker-compose, which can be used to easily setup a working development/testing environment for P4RROT.
To build and start the container use
```bash
docker compose run --rm p4rrot_dev  
```
The initial build process might take a few minutes. After it completes, you will be presented with the command line prompt inside a priviledged environment with your working directory mounted under `/nikss`.
> **Warning**
> The docker container runs with privileges and mounts the working directory. Be sure to backup any important data in this directory before starting the development process. 

The [pytest](https://docs.pytest.org/) based test scripts can be found inside the `/test` directory.
Running all tests in the directory can be achieved with
```bash
pytest . 
```
If you want to see additional logging messages, add `-log-cli-level=INFO`. 

You can also execute only a specific test file
```bash
pytest test_simulation.py
```
or even a specific test case
```bash
pytest test_simulation.py::test_assign_const
```



