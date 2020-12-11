const App = {
    data() {
        return {
            currentStep: 2,
            model: {
                selectedStep: 0,
            }
        }
    },
    methods: {
        getStepStatus(id) {
            if (id < this.currentStep) {
                return "finish";
            }
            else if (id == this.currentStep) {
                return "process";
            }
            else if (id > this.currentStep) {
                return "wait";
            }
            return "wait";
        }
    },
    computed: {
        selectedStep: {
            get() {
                return this.model.selectedStep;
            },
            set(newValue) {
                if (newValue > this.currentStep) {
                    this.$message.warning('Please complete this step first.');
                    newValue = this.currentStep;
                }
                this.model.selectedStep = newValue;
            }
        },
    },
    mounted() {
    }
};
var app = Vue.createApp(App).use(antd);
app.mount("#app");
