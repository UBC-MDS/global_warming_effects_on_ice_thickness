FROM rocker/tidyverse
# Install R
RUN apt-get update && \ 
    apt-get install r-base r-base-dev -y

RUN Rscript -e "install.packages('knitr')"
RUN Rscript -e "install.packages('tidyverse')"
RUN Rscript -e "install.packages('infer')"
RUN Rscript -e "install.packages('kableExtra')"
RUN Rscript -e "install.packages('svglite')"

# Install anaconda
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy && \
    /opt/conda/bin/conda update -n base -c defaults conda

# put anaconda python in path
ENV PATH="/opt/conda/bin:${PATH}"

# install python package
RUN conda install -y -c anaconda \ 
    docopt \
    requests \
    urllib3 \
    numpy \
    pandas \
    altair \
    scikit-learn \
    matplotlib

RUN conda install -c conda-forge altair_saver
RUN conda install -c conda-forge pandas-profiling
RUN conda install -c conda-forge python-chromedriver-binary 

# interactive
CMD ["/bin/bash"]