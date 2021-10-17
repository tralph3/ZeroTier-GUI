FROM debian:stable

RUN apt update -y

RUN apt install -y alien

WORKDIR /tmp

RUN mkdir img

RUN mkdir src

COPY src/ src

COPY zerotier-gui.desktop .

COPY make_deb.sh .

COPY README.md .

COPY LICENSE .

RUN chmod +x make_deb.sh

RUN ./make_deb.sh

RUN alien -r ZeroTier-GUI.deb && mv *.rpm ZeroTier-GUI.rpm