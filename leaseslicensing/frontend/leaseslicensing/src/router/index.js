//import Vue from 'vue'
import { createRouter } from 'vue-router'
import Profile from '@/components/user/profile.vue'
import external_routes from '@/components/external/routes'
import internal_routes from '@/components/internal/routes'

//Vue.use(Router)

const router = createRouter({
    mode: 'history',
    routes: [
        {
          path: '/firsttime',
          name: 'first-time',
          component: Profile
        },
        {
          path: '/account',
          name: 'account',
          component: Profile
        },
        external_routes,
        internal_routes,
    ]
})
