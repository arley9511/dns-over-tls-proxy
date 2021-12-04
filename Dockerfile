FROM gcr.io/distroless/python3

WORKDIR /app

COPY ./ /app

EXPOSE 53/tcp

EXPOSE 53/udp

CMD ["/app/src/main.py", "/etc"]
