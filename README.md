# CarlaAutonomousDriving

Reinforcement Learning course @ Warsaw University of Technology: CARLA autonomous driving

## How to start with CARLA?

1. Download [CARLA for Windows, v0.9.5]](http://carla-assets-internal.s3.amazonaws.com/Releases/Windows/CARLA_0.9.5.zip).
2. Extract the files into your desired location.
3. Create `CARLA_HOME` environment variable with `CARLA` path, e.g. `C:/Tools/CARLA_0.9.5`.
4. Run `CarlaUE4.exe` file from the root of extracted directory.
5. Use `W S A D` to move the camera. This opened window acts as a server.

## Python

- `Python 3.7.x`, e.g. [Python 3.7.5](https://www.python.org/downloads/release/python-375/)
- Upgrade `pip`: `python -m pip install --upgrade pip`
- Once installed, install Python requirements: `pip install -r requirements.txt`
- Check if `CARLA` is working by invoking a sample script, e.g. `python manual_driving.py`

## Links

[CARLA.org - main project page](http://carla.org/)
[Getting started with CARLA](https://carla.readthedocs.io/en/latest/getting_started/)
[Self-driving cars with Carla and Python](https://pythonprogramming.net/introduction-self-driving-autonomous-cars-carla-python/)
