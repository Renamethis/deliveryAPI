FROM node

COPY package.json /package.json
RUN npm install --only=prod
ADD . .
RUN npm run build