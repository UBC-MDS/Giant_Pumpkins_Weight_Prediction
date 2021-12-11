# Dockerfile for Giant Pumpkin Weight Prediction
# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-12-08


# Use rocker/tidyverse as the Base Image
FROM rocker/tidyverse@sha256:d0cd11790cc01deeb4b492fb1d4a4e0d5aa267b595fe686721cfc7c5e5e8a684


# Install R
RUN apt-get update

# Install R Packages
RUN Rscript -e "install.packages('knitr')"

# Solve Rscript warning by install libxt6
RUN apt-get install -y --no-install-recommends libxt6

# Install the Anaconda distribution of Python
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy && \
    /opt/conda/bin/conda update -n base -c defaults conda

# Put Anaconda Python in PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Install Python Packages
RUN /opt/conda/bin/conda install -y -c anaconda \
    docopt=0.6.* \
    altair=4.1.* 

# Install pandoc altair_saver
RUN /opt/conda/bin/conda install -y -c conda-forge pandoc altair_saver


CMD ["/bin/bash"]