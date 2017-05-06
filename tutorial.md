## Tutorial: Complexity Science

Allen Downey and Jason Woodard

This is a half-day tutorial that uses Python to introduce topics from Complexity
Science, including small world graphs and scale-free networks, cellular automata,
and agent-based models.  The tutorial is based on the book _Think Complexity_ and
on material from a class we teach at Olin College.


### Installation instructions

To prepare for this tutorial, you have two options:

1. Install Jupyter on your laptop and download my code from Git.

2. Run the Jupyter notebook on a virtual machine on Binder.

I'll provide instructions for both, but here's the catch: if everyone chooses Option 2,
the wireless network will fail and no one will be able to do the hands-on part of the workshop.

So, I strongly encourage you to try Option 1 and only resort to Option 2 if you can't get Option 1 working.

<!-- Allen, please feel free to move my following paragraph somewhere else. Contribution begin: -->
If you have the Anaconda distribution of Python setup, please run the following in your terminal:

```bash
$ conda env create -f environment.yml
$ source activate complexity
$ cd code/
$ jupyter notebook
```

<!-- Contribution end. -->

### Option 1A: If you already have Jupyter installed.

To do the exercises, you need Python 2 or 3 with NumPy, SciPy, and matplotlib.
If you are not sure whether you have those modules already, the easiest way to
check is to run my code and see if it works.

Code for this workshop is in a Git repository on Github.  
If you have a Git client installed, you should be able to download it by running:

    git clone https://github.com/AllenDowney/ThinkComplexity2.git

It should create a directory named `ThinkComplexity2`.
Otherwise you can download the repository in [this zip file](https://github.com/AllenDowney/ThinkComplexity2/zipball/gh-pages).

To start Jupyter, run:

    cd ThinkComplexity2/code
    jupyter notebook

Jupyter should launch your default browser or open a tab in an existing browser window.
If not, the Jupyter server should print a URL you can use.  For example, when I launch Jupyter, I get

    ~/ThinkComplexity2$ jupyter notebook
    [I 10:03:20.115 NotebookApp] Serving notebooks from local directory: /home/downey/ThinkComplexity2
    [I 10:03:20.115 NotebookApp] 0 active kernels
    [I 10:03:20.115 NotebookApp] The Jupyter Notebook is running at: http://localhost:8888/
    [I 10:03:20.115 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).

In this case, the URL is [http://localhost:8888](http://localhost:8888).  
When you start your server, you might get a different URL.
Whatever it is, if you paste it into a browser, you should should see a home page with a list of the
notebooks in the repository.

Click on `chap06.ipynb`.  It should open the notebook for Chapter 6.

Select the cell with the import statements and press "Shift-Enter" to run the code in the cell.
If it works and you get no error messages, **you are all set**.  

If you get error messages about missing packages, you can install the packages you need using your
package manager, or try Option 1B and install Anaconda.

For the animations in this notebook to work, you might have to install ffmpeg. On Ubuntu and Linux Mint,
the following should do it:

```
    sudo add-apt-repository ppa:mc3man/trusty-media
    sudo apt-get update
    sudo apt-get install ffmpeg
```
If you have instructions for other operating systems, please let me know and I will add them here.


### Option 1B: If you don't already have Jupyter.

I highly recommend installing Anaconda, which is a Python distribution that contains everything
you need for the workshop.  It is easy to install on Windows, Mac, and Linux, and because it does a
user-level install, it will not interfere with other Python installations.

[Information about installing Anaconda is here](http://docs.continuum.io/anaconda/install.html).

When you install Anaconda, you should get Jupyter by default, but if not, run

    conda install jupyter

Then go to Option 1A to make sure you can run my code.

If you don't want to install Anaconda,
[you can see some other options here](http://jupyter.readthedocs.io/en/latest/install.html).


### Option 2: only if Option 1 failed.

You can run my notebook in a virtual machine on Binder. To launch the VM, press this button:

 [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/allendowney/thinkcomplexity2)

You should see a home page with a list of the notebooks in the repository.

If you want to try the exercises, open `chap01.ipynb`. If you just want to see the answers, open `chap01soln.ipynb`.
Either way, you should be able to run the notebooks in your browser and try out the examples.  

However, be aware that the virtual machine you are running is temporary.
If you leave it idle for more than an hour or so, it will disappear along with any work you have done.

Special thanks to the generous people who run Binder, which makes it easy to share and reproduce computation.

### Option 3: If you have a Mac and are willing to try something new

Launchbot is a tool being developed within O'Reilly Media to make it simple to build and run Jupyter-based projects. It's basically a GUI for git, Docker, and Jupyter:

<img src="https://launchbot.io/images/launchbot-client.gif"/>

To run the project with Launchbot, you must:

* Install docker
* Install and configure the launchbot app

#### Install and start Docker

Before you can use LaunchBot, you'll need to install [Docker for Mac](https://www.docker.com/products/docker-engine)

Docker allows you "containerize" applications. Launchbot uses it to build and run the underlying environment required for your application to function.

*IMPORTANT*: Docker must be running to use LaunchBot, so you'll need to make sure it's started each time you want to use LaunchBot.  On a Mac, you'll see the Docker "whale" icon in the Menubar.

<img src="http://launchbot.io/docs/images/docker-mac-toolbar.png"/>

You will get the following error in Launchbot if Docker is not running:

```
Cannot connect to the docker engine endpoint
```

#### Install and Configure the Launchbot App

Download and unzip LaunchBot from https://launchbot.io

#### Clone The Project

Once the Launchbot app is running, you can clone the  repository from the list of projects on the main screen.  Be sure to use the `https` url.

#### Launch the Project

Once it's cloned, open it from the "Your Projects" list.  Then click "Launch".  

*IMPORTANT*: The first time you build a project, Launchbot must download and build the entire image.  Since these images are often quite large, this can take several minutes.  

#### Get Your Jupyter Access token from the container log

Jupyter password protects the Notebooks by default.  To find your password, click the "Log" button.  Scroll down until you find a line like this:

```
To login with a token:
       http://localhost:8888/?token=00e6b380dddd53b77649f6a533a2407db1996f44b6b9e325
```

Copy just the token (in this case, `00e6b380dddd53b77649f6a533a2407db1996f44b6b9e325`) and then paste it into the prompt for the notebook.
