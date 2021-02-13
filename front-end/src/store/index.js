import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loggedUser: {}
  },
  mutations: {
    setUser: (state, user) => {
      state.loggedUser = user
    }
  },
  actions: {
    updateUser: ({ commit }, user) => {
      commit('setUser', user)
    }
  }
})