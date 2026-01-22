## **ROADMAP BACKEND ATUALIZADO – FINZIA (MVP)**

| # | Módulo / Funcionalidade | Status | Observações / Pendências | Próximo passo |
| --- | --- | --- | --- | --- |
| **1** | Estrutura / Core (DB, Models, Conexão dinâmica) | ✅ Concluído | - | Manutenção |
| **2** | CRUD Contas, Categorias, Despesas, Receitas | ✅ Concluído | - | Ajustes finos se necessário |
| **3** | 3.6 – Saúde Financeira | ✅ Concluído | Mensagens refinadas | - |
| **4** | 3.8 – Score Financeiro | ✅ Concluído | Thresholds ajustados | - |
| **5** | 3.9 – Previsão Financeira | ✅ Concluído | Parâmetros calibrados | - |
| **6** | 3.11 – Risco de Endividamento Futuro | ✅ Concluído | Valores de projeção calibrados | - |
| **7** | 3.13 – Otimização de Orçamento | ✅ Concluído | Regras progressivas aplicadas | - |
| **8** | 3.16 – Missões Financeiras | ✅ Concluído | - | - |
| **9** | 3.18 – Alertas por Categoria | ✅ Concluído | Thresholds calibrados | - |
| **10** | 3.19 – Alertas por Metas de Categoria | ✅ Concluído | Alertas duplicados corrigidos | - |
| **11** | 3.21 – Estrutura de envio de alertas | ✅ Concluído | - | - |
| **12** | 3.22 – Envio automático e manual (E-mail / WhatsApp Web) | ✅ Concluído | Mensagens longas adaptadas | - |
| **13** | 3.23 – Alertas por despesas fora do padrão | ✅ Concluído | Lógica de anomalias implementada | - |
| **14** | 3.24 – Dashboards e relatórios avançados | ✅ Concluído | Endpoints prontos para frontend | - |
| **15** | 3.25 – Ajuste do motor de inteligência | ✅ Concluído | Heurísticas calibradas | - |
| **16** | 3.26 – Integração ERP / importação de dados | ✅ Concluído | Conector dinâmico implementado | - |

### **Resumo do MVP (backend + motor de inteligência)**

- **Todas as funcionalidades (3.6 a 3.26) implementadas e testadas ✅**
- **Alertas calibrados, dashboards prontos, motor de inteligência ajustado ✅**
- **Backend pronto para integração com frontend ✅**

**Percentual de conclusão do MVP:** 100%

## **ROADMAP DO FRONTEND – FINZIA (Vue.js + Tailwind + JWT)**

---

### **FASE 0 – Configuração Inicial**

**Objetivo:** Preparar ambiente desacoplado, pronto para desenvolvimento e Docker.

| Tarefa | Descrição | Status | Observações |
| --- | --- | --- | --- |
| Criar projeto Vue.js 3 | `npm init vue@latest` ou `yarn create vue` | ✅ Concluído | Nome: `finzia-frontend` |
| Instalar dependências básicas | Vue Router, Pinia (state), Axios | ✅ Concluído | Compatível com Vue 3 |
| Configurar TailwindCSS | Estilização responsiva e rápida | ✅ Concluído | Incluindo gradientes, cores da marca |
| Configurar ESLint / Prettier | Padronização de código | ✅ Concluído | Regras básicas aplicadas |
| Criar Dockerfile e docker-compose | Contêiner isolado para front | ✅ Concluído | Conectado com backend via rede Docker |

**Resultado esperado:** Projeto Vue.js inicial rodando em Docker, pronto para desenvolver páginas.

---

### **FASE 1 – Autenticação (Login / Logout / JWT)**

**Objetivo:** Implementar autenticação completa usando JWT gerado pelo backend.

| Tarefa | Descrição | Status | Observações |
| --- | --- | --- | --- |
| Criar página de Login | Formulário com e-mail/usuário + senha | ✅ Concluído | Axios simulado / frontend pronto |
| Armazenar token | LocalStorage / Pinia | ✅ Concluído | Interceptores podem ser adicionados futuramente |
| Criar logout | Remover token + redirecionar | ✅ Concluído | Limpeza de store + localStorage implementada |
| Proteger rotas | Route guards para dashboard, despesas, etc | ✅ Concluído | Rotas públicas e privadas configuradas |
| Refresh token (opcional) | Implementar fluxo se backend suportar | ✅ Concluído | Placeholder pronto para backend |

**Resultado esperado:** Login funcional, logout, JWT armazenado e rotas protegidas.

---

### **FASE 2 – CRUD Contas, Categorias, Despesas e Receitas**

**Objetivo:** Consumir endpoints existentes do backend.

| Tarefa | Descrição | Status | Observações |
| --- | --- | --- | --- |
| Listagem | Tabelas de contas, categorias, despesas, receitas | 🔲 | Paginação e filtros |
| Criação | Forms para adicionar registros | 🔲 | Validação de dados (vuelidate ou composables) |
| Edição | Forms pré-preenchidos para atualizar | 🔲 | Incluindo user_id via JWT |
| Exclusão | Botão de remover com confirmação | 🔲 | Feedback visual (toast) |
| Filtros avançados | Por data, categoria, valor | 🔲 | Usar `Query params` para backend |

**Resultado esperado:** CRUD completo para o usuário com feedback visual e integração total com backend.

---

### **FASE 3 – Dashboards e KPIs**

**Objetivo:** Criar visualizações interativas consumindo os endpoints do backend.

| Tarefa | Descrição | Status | Observações |
| --- | --- | --- | --- |
| Dashboard principal | Saúde financeira, score, risco futuro | 🔲 | Cards resumidos e progress bars |
| Gráficos de despesas e receitas | Linha, barra ou pizza (chart.js ou ECharts) | 🔲 | Filtros por período |
| Alertas em tempo real | Exibir alertas 3.6 a 3.23 | 🔲 | Componentes de lista com cores por prioridade |
| Otimização de orçamento | Visualizar recomendações do backend | 🔲 | Highlight de categorias críticas |
| Missões financeiras | Cards interativos com status | 🔲 | Integrar lógica do backend |

**Resultado esperado:** Dashboard interativo, responsivo, com dados dinâmicos e alertas visuais.

---

### **FASE 4 – Alertas, Notificações e Interações**

**Objetivo:** Mostrar alertas detalhados, envio manual e filtros por usuário/categoria.

| Tarefa | Descrição | Status | Observações |
| --- | --- | --- | --- |
| Lista de alertas | Filtrável por categoria, tipo, nível | 🔲 | Integração com backend |
| Visualização de detalhes | Modal ou página dedicada | 🔲 | Mostrar valor, threshold e data |
| Ações rápidas | Marcar como lido, ignorar ou reenviar | 🔲 | Atualiza backend via PATCH/PUT |
| Notificações | Toast ou snackbar para alertas novos | 🔲 | Pode usar Pinia para estado global |

**Resultado esperado:** Alertas interativos, em tempo real, filtráveis e gerenciáveis.

---

### **FASE 5 – Integração ERP e Importação de Dados**

**Objetivo:** Criar interface para importar lançamentos do ERP.

| Tarefa | Descrição | Status | Observações |
| --- | --- | --- | --- |
| Upload de arquivos | CSV, Excel ou conexão direta (se suportado) | 🔲 | Formulário seguro |
| Mapeamento de campos | Seleção de colunas correspondentes | 🔲 | Ex.: categoria, conta, valor, data |
| Feedback visual | Progress bar e logs de importação | 🔲 | Erros e alertas destacados |
| Histórico de importações | Página/lista de uploads | 🔲 | Integrar com backend |

**Resultado esperado:** Importação ERP fácil, segura e visualmente clara para o usuário.

---

### **FASE 6 – Testes e Ajustes Finais**

**Objetivo:** Garantir estabilidade, responsividade e performance.

| Tarefa | Descrição | Status | Observações |
| --- | --- | --- | --- |
| Testes de fluxo | Login, CRUD, dashboards, alertas | 🔲 | Garantir que tudo funcione com JWT |
| Testes mobile | Responsividade e layout | 🔲 | Tailwind facilita ajustes |
| Testes de performance | Charts e endpoints pesados | 🔲 | Otimizar chamadas Axios |
| Ajustes finais de UX/UI | Feedbacks visuais, cores, mensagens | 🔲 | Tornar uso intuitivo e agradável |

**Resultado esperado:** Frontend pronto para usuários, totalmente desacoplado, interativo e responsivo.

Dockerfile Front

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev"]


version: "3.9"

services:
  # ===============================
  # Backend (FastAPI)
  # ===============================
  api:
    build: ./backend
    container_name: finance-api
    restart: always
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: mysql+mysqlconnector://finance_user:user123@db:3306/finance_db
    networks:
      - finance-net

  # ===============================
  # Banco de Dados (MySQL)
  # ===============================
  db:
    image: mysql:8.0
    container_name: finance-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: finance_db
      MYSQL_USER: finance_user
      MYSQL_PASSWORD: user123
    ports:
      - "3306:3306"
    volumes:
      - finance_db_data:/var/lib/mysql
    networks:
      - finance-net

  # ===============================
  # Frontend (Vue.js)
  # ===============================
  app:
    build: ./frontend
    container_name: finance-app
    restart: always
    ports:
      - "5173:5173"  # expõe a porta para o host
    environment:
      - CHOKIDAR_USEPOLLING=true
    command: ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
    depends_on:
      - api
    networks:
      - finance-net

# ===============================
# Volumes
# ===============================
volumes:
  finance_db_data:

# ===============================
# Network
# ===============================
networks:
  finance-net:
    driver: bridge
