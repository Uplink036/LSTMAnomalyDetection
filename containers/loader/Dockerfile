FROM python
RUN mkdir /logs
WORKDIR /loader
COPY . .
RUN pip install -r requirments.txt
ENV DATABASE_URL=mongodb://localhost:27017/
ENV SCRUB_DB=0
CMD ["./run.sh"]