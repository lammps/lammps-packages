FROM lammps/lammps:patch_8Apr2021_ubuntu20.04_openmpi_py3
MAINTAINER richard.berger@outlook.com

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade jupyterlab pandas numpy matplotlib
RUN ln -s /lib/x86_64-linux-gnu/liblammps_serial.so /lib/x86_64-linux-gnu/liblammps.so
RUN mkdir -p /usr/local/share/jupyter/lab/settings

ADD jupyterlab/.bash_profile /home/lammps/.bash_profile
ADD jupyterlab/README.md /home/lammps/
ADD lammps/examples /home/lammps/examples
ADD lammps/python/examples/pylammps /home/lammps/pylammps-examples
ADD jupyterlab/jupyter_lab_config.py /home/lammps/.jupyter/jupyter_lab_config.py
ADD jupyterlab/overrides.json /usr/local/share/jupyter/lab/settings/overrides.json
RUN chown -R lammps:lammps examples pylammps-examples .jupyter .bash_profile

USER lammps
WORKDIR /home/lammps

EXPOSE 8888

ENV SHELL="/bin/bash"

CMD jupyter lab --ip 0.0.0.0 --port 8888
