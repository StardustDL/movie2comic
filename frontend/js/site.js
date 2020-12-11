// const PREPURL = "";
const PREPURL = "http://localhost:5050" // Debug

const App = {
    data() {
        return {
            sessionId: null,
            currentStep: 0,
            model: {
                selectedStep: 0,
            },
            apiUrl: PREPURL,
            pages: {
                p0: {
                    inputFile: null,
                }
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
        },
        onUploadChange(event) {
            if (event.file.status !== 'uploading') {
            }
            if (event.file.status === 'done') {
                this.sessionId = event.file.response;
                this.currentStep = 1;
                this.model.selectedStep = 1;
                this.$message.success(`${event.file.name} file uploaded successfully`);
            } else if (event.file.status === 'error') {
                this.$message.error(`${event.file.name} file upload failed.`);
            }
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
