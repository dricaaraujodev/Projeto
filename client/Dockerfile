FROM golang:1.20-bullseye AS build

# Install libzmq dev for cgo bindings
RUN apt-get update && apt-get install -y --no-install-recommends libzmq3-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY go.mod ./
RUN go mod download

COPY client.go ./
RUN go get github.com/pebbe/zmq4
RUN CGO_ENABLED=1 go build -o bbs-client client.go

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends libzmq3-dev && rm -rf /var/lib/apt/lists/*WORKDIR /app
COPY --from=build /app/bbs-client /app/bbs-client
CMD ["/app/bbs-client"]
