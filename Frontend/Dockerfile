FROM node:18

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install next

COPY . .

RUN npm run build

EXPOSE 5004

CMD npm run start