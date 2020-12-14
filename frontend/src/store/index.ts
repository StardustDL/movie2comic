import { createStore } from 'vuex'
import { SessionStage, SessionState } from "../models/enum"

export default createStore({
  state() {
    return {
      state: SessionState.AfterCreate,
      stage: SessionStage.Create,
      sessionId: "",
      apiUrl: ""
    }
  },
  getters: {
    sessionRootUrl(state: any) {
      return `${state.apiUrl}/api/session`;
    },
    sessionUrl(state: any, getters: any) {
      return `${getters.sessionRootUrl}/${state.sessionId}`;
    },
  },
  mutations: {
    setApi(state, value) {
      state.apiUrl = value;
    },
    setSession(state, value) {
      state.sessionId = value;
    },
    setState(state, value) {
      state.state = value;
    },
    setStage(state, value) {
      state.stage = value;
    }
  },
  actions: {
    updateState(context) {
      const { state, getters } = context;
      if (state.sessionId) {
        fetch(`${getters.sessionUrl}/state`).then(res => res.text()).then(value => {
          context.commit("setState", parseInt(value))
        });
        fetch(`${getters.sessionUrl}/stage`).then(res => res.text()).then(value => {
          context.commit("setStage", parseInt(value))
        });
      }
    },
    autoUpdate(context) {
      setInterval(() => {
        if (context.state.sessionId) {
          context.dispatch("updateState");
        }
        else {
          context.commit("setState", 0);
          context.commit("setStage", 0);
        }
      }, 2000);
    }
  },
  modules: {
  }
})
