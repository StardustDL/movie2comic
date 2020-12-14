<template>
  <a-space direction="vertical" style="width: 100%">
    <div id="home-readme">
      <a-spin tip="Loading homepage..." size="large" style="width: 100%">
        <div style="min-height: 50vh"></div>
      </a-spin>
    </div>
    <div style="text-align: right">
      <h1>
        StardustDL -
        <a href="https://github.com/StardustDL/movie2comic"
          ><span class="mdi mdi-github"></span> GitHub</a
        >
      </h1>
    </div>
    <div>
      <a-button type="primary" size="large" @click="onStart" style="width: 100%"
        >Start</a-button
      >
    </div>
  </a-space>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import VditorPreview from "vditor";
import "vditor/dist/index.css";
import { StepPageNames } from "@/models/enum";

export default defineComponent({
  name: "Home",
  components: {},
  data() {
    return {};
  },
  methods: {
    onStart() {
      this.$router.replace({ name: StepPageNames.Start });
    },
  },
  mounted() {
    fetch(
      "https://raw.githubusercontent.com/StardustDL/movie2comic/master/README.md"
    )
      .then((response) => response.text())
      .then((text) => {
        VditorPreview.preview(
          document.getElementById("home-readme") as HTMLDivElement,
          text
        );
      });
  },
});
</script>
