import { createStore } from 'vuex'
import { SessionStage, SessionState } from "../models/enum"

export default createStore({
  state() {
    return {
      state: SessionState.AfterCreate,
      stage: SessionStage.Create,
    }
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
