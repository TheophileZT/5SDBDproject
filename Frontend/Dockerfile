FROM node:18

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install next

EXPOSE 3000

CMD npm run dev