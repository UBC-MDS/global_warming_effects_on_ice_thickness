FROM rocker/tidyverse

RUN apt-get update 

# install make
RUN apt-get install make

# install R
RUN apt-get install r-base r-base-dev -y

# intall R libraries
RUN Rscript -e "install.packages('knitr')"
RUN Rscript -e "install.packages('tidyverse')"
RUN Rscript -e "install.packages('infer')"
RUN Rscript -e "install.packages('kableExtra')"
RUN Rscript -e "install.packages('svglite')"

# install anaconda
RUN wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    . /opt/conda/bin/activate && \
    conda init

ENV PATH="/opt/conda/bin:${PATH}"

# install python packages from anaconda channel
RUN conda install -y -c anaconda \ 
    docopt \
    requests \
    urllib3 \
    numpy \
    pandas \
    altair

# install python packages from conda-forge channel
RUN conda install -y -c conda-forge \
    altair_saver \
    pandas-profiling \
    python-chromedriver-binary

# interactive
CMD ["/bin/bash"]