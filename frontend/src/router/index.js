// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ===== Views =====
import WelcomeView from '@/views/WelcomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ProfileSettings from '@/views/ProfileSettings.vue'
import UsersView from '@/views/UsersView.vue'
import CategoriesView from '@/views/CategoriesView.vue'
import AccountsView from '@/views/AccountsView.vue'
import ExpensesView from '@/views/ExpensesView.vue'
import IncomesView from '@/views/IncomesView.vue'

const routes = [
  { path: '/', redirect: '/welcome' },
  { path: '/welcome', name: 'Welcome', component: WelcomeView }, // pública
  { path: '/login', name: 'Login', component: LoginView }, // pública
  { path: '/register', name: 'Register', component: RegisterView }, // pública
  { path: '/dashboard', name: 'Dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/profile', name: 'ProfileSettings', component: ProfileSettings, meta: { requiresAuth: true } },
  { path: '/users', name: 'Users', component: UsersView, meta: { requiresAuth: true } },
  { path: '/categories', name: 'Categories', component: CategoriesView, meta: { requiresAuth: true } },
  { path: '/accounts', name: 'Accounts', component: AccountsView, meta: { requiresAuth: true } },
  { path: '/expenses', name: 'Expenses', component: ExpensesView, meta: { requiresAuth: true } },
  { path: '/incomes', name: 'Incomes', component: IncomesView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// ===== Guard Global =====
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  // Se houver token mas Pinia ainda não carregou o usuário, busca do backend
  if (!auth.user && localStorage.getItem('token')) {
    try {
      await auth.fetchUser()
    } catch (err) {
      console.warn('Token inválido ou expirado, redirecionando para login...')
      auth.logout()
      return next('/login')
    }
  }

  const requiresAuth = to.meta.requiresAuth || false

  // Protege rotas privadas
  if (requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }

  // Impede usuário logado de acessar login/register
  if ((to.path === '/login' || to.path === '/register') && auth.isAuthenticated) {
    return next('/dashboard')
  }

  next()
})

export default router
