FROM node:18

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install next

COPY . .

EXPOSE 3000

CMD npm run dev