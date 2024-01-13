FROM node:16-alpine3.11

WORKDIR /usr/src/app
COPY ./src/package*.json ./
RUN npm install
COPY ./src .

CMD ["node", "app"]
