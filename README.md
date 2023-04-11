# Enchanted Motorbike

A demo Python project that can teach you:

- A basic asynchronous HTTP server.
- A simple synchronous TCP server.
- Asynchronous TCP client based on `asyncio`.
- Typed repositories - almost like in _The Clean Architecture_, but less
  clean. ![](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)
- Fun MongoDB aggregate requests and even more fun MongoDB's
  stupid issues. ![](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

## How to run

### Requirements

You need Python 3.10 or newer to run this project.

First, make a new poetry environment and do `poetry install` to resolve dependencies.

### Components

The project consists of three modules - sensor, controller, and manipulator.
To run each module independently, execute one of the following commands:

```bash
python -m enchanted_motorbike --sensor
python -m enchanted_motorbike --controller
python -m enchanted_motorbike --manipulator
```

Short description of components:

- Sensor - generates some random XY coordinates and sends them to the HTTP server.
- Controller - an HTTP server that gathers data from sensors, "analyzes" it, and decides a new Manipulator state.
- Manipulator - controlled by the Controller (ha), it receives signals over TCP. It could change its state somehow, but
  all it does is logging received signals to console.

### Docker (Compose)

Simply run `docker compose up --build` to build the Docker image and run all containers.
A single image is shared between multiple containers thanks to the `command` option.

Press `Ctrl+C` to gracefully stop the system.
Run `docker compose down -v` to fully clean up.
Avoid the `-v` option if you want to delete containers
but preserve the local storage and the signal history.   