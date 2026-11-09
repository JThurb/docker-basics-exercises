# Simple button

## How to start

# Install java
FROM amazoncorretto:8

EXPOSE 8080

WORKDIR /usr/src/app

COPY . .

RUN ./mvnw package

CMD ["java", "-jar", "./target/docker-example-1.1.3.jar"]
# Make sure you have java 8 installed

# Build the project with `./mvnw package`

# Run with `java -jar ./target/docker-example-1.1.3.jar`

# The project should open in `8080` and you get a message by pressing the button.
