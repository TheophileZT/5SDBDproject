FROM node:18

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install next

EXPOSE 5004

CMD npm run dev