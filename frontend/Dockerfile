FROM node:22-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Build the app (for production)
# RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "dev"]
