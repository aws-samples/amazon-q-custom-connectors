FROM python:3.12.3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./documents
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/analytics-lens/analytics-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/container-build-lens/container-build-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/government-lens/government-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/healthcare-industry-lens/healthcare-industry-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/iot-lens/wellarchitected-iot-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/machine-learning-lens/wellarchitected-machine-learning-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/saas-lens/wellarchitected-saas-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/serverless-applications-lens/wellarchitected-serverless-applications-lens.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/framework/wellarchitected-framework.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/cost-optimization-pillar/wellarchitected-cost-optimization-pillar.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/operational-excellence-pillar/wellarchitected-operational-excellence-pillar.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/performance-efficiency-pillar/wellarchitected-performance-efficiency-pillar.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/reliability-pillar/wellarchitected-reliability-pillar.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/sustainability-pillar/wellarchitected-sustainability-pillar.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/security-pillar/wellarchitected-security-pillar.pdf
RUN wget -P ./documents https://docs.aws.amazon.com/pdfs/wellarchitected/latest/operational-readiness-reviews/operational-readiness-reviews.pdf

COPY ./server.py ./

ENTRYPOINT ["python3"]
CMD ["/usr/src/app/server.py"]

