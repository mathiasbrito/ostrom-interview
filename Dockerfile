FROM python:alpine as build

COPY . /app
WORKDIR /app

RUN python setup.py sdist bdist_wheel

FROM python:slim

COPY --from=build /app/dist /app-pkg
RUN pip install /app-pkg/*.whl

CMD ["ostrom"]

