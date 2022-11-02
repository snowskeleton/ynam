FROM selenium/standalone-chrome as b1

ENV PATH=$HOME/.local/bin:$PATH

RUN sudo su
RUN echo "**** install packages ****" && \
    sudo apt-get update && \
    sudo apt-get install -y python3-pip git && \
    echo "**** cleanup ****" && \
    sudo apt-get clean && \
    sudo rm -rf \
    /tmp/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

FROM b1 as b2
RUN sudo pip3 install -e git+https://github.com/snowskeleton/mintapi#egg=mintapi

FROM b2
COPY . ./ynam/
RUN cd ynam && sudo pip3 install .
ENTRYPOINT ["sudo","ynam", "--use-chromedriver-on-path"]
# CMD sudo ls -laf /root
# CMD ["-h"]
