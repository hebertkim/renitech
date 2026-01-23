# frontend/Dockerfile
FROM node:20-alpine

# Diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar todo o código
COPY . .

# Expor porta do dev server Vue.js
EXPOSE 5173

# Rodar Vue.js com hot reload e host 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
