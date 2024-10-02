FROM continuumio/miniconda3


RUN mkdir /tmp/testcywebserviceapp
COPY dist/*.whl /tmp/testcywebserviceapp/

RUN pip install /tmp/testcywebserviceapp/testcywebserviceapp*whl

RUN rm -rf /tmp/testcywebserviceapp

ENTRYPOINT ["/opt/conda/bin/testcywebserviceappcmd.py"]
CMD ["--help"]
