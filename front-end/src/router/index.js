import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import RegistrationForm from '../views/RegistrationForm.vue'
import Event from '../views/Event.vue'
import NewEventForm from '../views/NewEventForm.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/new_event',
    name: 'NewEvent',
    component: NewEventForm
  },
  {
    path: '/event/:event_id',
    name: 'Event',
    component: Event
  },
  {
    path: '/registration',
    name: 'Registration',
    component: RegistrationForm
  }
]

const router = new VueRouter({
  routes
})

export default router
