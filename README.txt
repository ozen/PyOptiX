This is not completed project

requires Optix and Cuda for compile

requires Boost.Numpy ubuntu package for compilation
look installation in https://bitbucket.org/imcom/boost.numpy

Issues:
* setup.py only install the cpp project not project itself. This is crutial for developing and deploying easy thing.
* compiler setup configuration is hard coded. It should be outside of package
* compiler looks only cu file. If cu file changes it compile again, but not included files like cuh files
* some parts connected directly c++ project, It should written python reflection

