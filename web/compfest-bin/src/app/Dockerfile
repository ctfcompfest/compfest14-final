FROM python:3.10.6

RUN apt update
RUN apt install -y libcairo-dev libpango1.0-dev libgdk-pixbuf2.0-dev
RUN apt install -y build-essential

COPY src /var/compfestbin

RUN pip install -r /var/compfestbin/requirements.txt

WORKDIR /var/compfestbin
ADD ./db3485d0f1bc54303cdaf9dabb1d78d961e50b233efeec9e663aea5df89490f5.db /var/compfestbin/db3485d0f1bc54303cdaf9dabb1d78d961e50b233efeec9e663aea5df89490f5.db

RUN useradd -ms /bin/bash ctf
RUN chown ctf:ctf /var/compfestbin/db3485d0f1bc54303cdaf9dabb1d78d961e50b233efeec9e663aea5df89490f5.db /var/compfestbin
RUN chmod 777 /var/compfestbin/db3485d0f1bc54303cdaf9dabb1d78d961e50b233efeec9e663aea5df89490f5.db

USER ctf

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]
