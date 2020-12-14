import { ComponentCustomProperties } from 'vue'
import { Store } from 'vuex'
import { SessionStage, SessionState } from "./models/enum"

declare module '@vue/runtime-core' {
  // declare your own store states
  interface State {
    state: SessionState,
    stage: SessionStage,
    sessionId: string,
    apiUrl: string,
  }

  // provide typings for `this.$store`
  interface ComponentCustomProperties {
    $store: Store<State>
  }
}