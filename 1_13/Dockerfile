# Base image
FROM golang:1.16

# port variablena
ENV PORT=8080

# request origin
ENV REQUEST_ORIGIN=https://example.com

# working directory
WORKDIR /usr/src/app

# Install golang
RUN curl https://golang.org/doc/install

# copy app code
COPY . .

# Expose port
EXPOSE $PORT

#Run "go build"
RUN go build

# Run test
RUN go test ./...

# Execute project
CMD ["./server"]
