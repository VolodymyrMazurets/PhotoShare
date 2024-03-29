FROM node:20

WORKDIR /app

COPY package*.json .

RUN npm install --no-cache

COPY . .

CMD ["npm", "run", "dev"]

