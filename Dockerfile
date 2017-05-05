FROM jupyter/scipy-notebook:latest

USER root
# ffmpeg is no longer available in Jesse: https://wiki.debian.org/ffmpeg
# However, it is in backports
# This Dockerfile installs it; from https://hub.docker.com/r/themylogin/docker-ffmpeg/~/dockerfile/
RUN sed -i "s/jessie main/jessie main contrib non-free/" /etc/apt/sources.list
RUN echo "deb http://http.debian.net/debian jessie-backports main contrib non-free" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y \
    ffmpeg
USER jovyan

# Launchbot labels
LABEL name.launchbot.io="ThinkDSP"
LABEL workdir.launchbot.io="/usr/workdir"
LABEL 8888.port.launchbot.io="Jupyter Notebook"

# Set the working directory
WORKDIR /usr/workdir

# Expose the notebook port
EXPOSE 8888

# Start the notebook server
CMD jupyter notebook --no-browser --port 8888 --ip=*