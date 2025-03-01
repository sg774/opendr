from setuptools import setup
from setuptools import find_packages
from Cython.Build import cythonize

packages = find_packages(where="./src")

with open('requirements.txt') as fp:
    install_requires = fp.read().splitlines()

exec(open('src/opendr/_version.py').read())

try:
    __version__
except NameError:
    __version__ = '0.0'

setup(
    name='opendr-toolkit',
    version=__version__,
    description='Open Deep Learning Toolkit for Robotics',
    long_description="""The aim of OpenDR is to develop a modular, open and non-proprietary toolkit for core
                     robotic functionalities by harnessing deep learning to provide advanced perception and
                     cognition capabilities, meeting in this way the general requirements of robotics
                     applications in the applications areas of healthcare, agri-food and agile production.
                     The term toolkit in OpenDR refers to a set of deep learning software functions, packages
                     and utilities used to help roboticists to develop and test a robotic application that
                     incorporates deep learning. OpenDR will provide the means to link the robotics applications
                     to software libraries (deep learning frameworks, e.g., Tensorflow) and to link it with the
                     operating environment (ROS). OpenDR focuses on the AI and Cognition core technology in order
                     to provide tools that make robotic systems cognitive, giving them the ability to a) interact
                     with people and environments by developing deep learning methods for human centric and
                     environment active perception and cognition, b) learn and categorise by developing deep
                     learning tools for training and inference in common robotics settings, and c) make decisions
                     and derive knowledge by developing deep learning tools for cognitive robot action and
                     decision making (WP5). As a result, the developed OpenDR toolkit will also enable cooperative
                     human-robot interaction as well as the development of cognitive mechatronics where sensing
                     and actuation are closely coupled with cognitive systems thus contributing to another two
                     core technologies beyond AI and Cognition. OpenDR will develop, train, deploy and evaluate
                     deep learning models that improve the technical capabilities of the core technologies beyond
                     the current state of the art. It will enable a greater range of robotics applications that
                     can be demonstrated at TRL 3 and above, thus lowering the technical barriers within the
                     prioritised application areas. OpenDR aims to an easily adopted methodology to adapt the
                     provided tools in order to solve any robotics task without restricting it to any specific
                     application""",
    author='OpenDR consortium',
    author_email='tefas@csd.auth.gr',
    packages=packages,
    url='https://github.com/opendr-eu/opendr',
    license='LICENSE',
    package_dir={"": "src"},
    install_requires=install_requires,
    ext_modules=cythonize(["src/opendr/perception/object_detection_2d/retinaface/algorithm/cython/*.pyx"])
)
