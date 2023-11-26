# Use an official Node runtime as a parent image
FROM node:14-alpine as builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project to the working directory
COPY . .

# Set environment variables for the build
ARG API_BASE_URL
ARG BACKEND_BASE_URL
ENV REACT_APP_API_BASE_URL=${API_BASE_URL}
ENV REACT_APP_BACKEND_BASE_URL=${BACKEND_BASE_URL}

# Build the React app
RUN npm run build

# Use a smaller base image for the production environment
FROM node:14-alpine

# Set the working directory to the app directory
WORKDIR /app

# Copy the build artifacts from the builder stage to the app directory
COPY --from=builder /app/build ./build

# Expose port 3000 for the React app
EXPOSE 3000

# Command to run on container start
CMD ["npx", "serve", "-s", "build"]