# ubuntu
FROM ubuntu:24.04

EXPOSE 5001

WORKDIR /usr/src/app

# update apt-get and install curl

RUN apt-get update && apt-get install -y curl

# install node.js
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs 

# check install
RUN node -v && npm -v

# Copy package.json and package-lock.json first to leverage caching
COPY package*.json ./

# install packages
RUN npm install

COPY . .

# build static files 
RUN npm run build

# install serve 
RUN npm install -g serve

CMD ["serve", "-s", "-l", "5001", "build"]


