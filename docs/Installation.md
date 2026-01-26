## Installation

Follow [windows_installation](./docs/Install_windows.md) for Windows Users .

- Install [osmium](https://github.com/osmcode/pyosmium) lib on your machine

```
pip install osmium
```

- Install osmsg

```
pip install osmsg
```

### Development 

Fork the repo https://github.com/kshitijrajsharma/OSMSG.git

Then clone your fork:

```
git clone https://github.com/[Your github profile name]/[The repo name you choose].git
```

**If you use Debian based Linux distros, make sure the following system libraries and tools are installed**

```
build-essential - Provices gcc, g++ and make for compiling C/C++ code (https://packages.ubuntu.com/jammy/build-essential)
clang - C/C++ compiler. Required by packages like 'pyproj' for building extensions on some systems.
cmake - Needed for osmium (https://github.com/osmcode/pyosmium)
libproj-dev - Needed for Geopandas (https://github.com/geopandas/geopandas?tab=readme-ov-file)
proj-bin - Needed for Geopandas (https://github.com/geopandas/geopandas?tab=readme-ov-file)
libgeos-dev - Needed for for Shapely and GeoPandas (Boost C++ libraries).
libboost-dev - Needed for for osmium (Boost C++ libraries).
libboost-system-dev - Needed for for osmium (Boost C++ libraries).
libboost-filesystem-dev - Needed for for osmium (Boost C++ libraries).
python3-dev - Provides Python headers for building Python extensions.
```

In the terminal, you can run

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake libproj-dev proj-bin libgeos-dev libboost-dev libboost-system-dev libboost-filesystem-dev python3-dev clang
```

Install PDM (python package and dependency manager), go to https://pdm-project.org/en/latest/#__tabbed_3_5
and follow the instructions.


### [DOCKER] Install with Docker locally

- Clone repo & Build Local container : 

  ```
  docker build -t osmsg:latest .
  ```

- Run Container terminal to run osmsg commands: 

  ```
  docker run -it osmsg
  ```

  Attach your volume for stats generation if necessary 

  ```
  docker run -it -v /home/user/data:/app/data osmsg
  ```

