FROM node:18

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install next

EXPOSE 5004

RUN npm run dev