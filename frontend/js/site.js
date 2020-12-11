// const PREPURL = "";
const PREPURL = "http://localhost:5050" // Debug

const App = {
    data() {
        return {
            sessionId: "9a7dc7b3-3b97-11eb-b47a-c83dd4eac83a",
            currentStep: 1,
            model: {
                selectedStep: 0,
            },
            apiUrl: PREPURL,
            pages: {
                p0: {
                    inputFile: null,
                },
                p1: {
                    frames: []
                }
            }
        }
    },
    methods: {
        readableSecondTimeString(value) {
            let minute = Math.floor(value / 60);
            let second = Math.floor(value % 60);
            if (minute == 0) {
                return `${second}''`;
            }
            else if (second == 0) {
                return `${minute}'`;
            }
            else {
                return `${minute}'${second}''`;
            }
        },
        onStartKeyframeExtractor() {
            this.startKeyframeExtractor();
        },
        onGetFrames() {
            this.getKeyframes();
        },
        async startKeyframeExtractor() {
            let settings = {
                method: 'PUT',
            };
            await fetch(`${this.apiUrl}/api/session/${this.sessionId}/keyframes`, settings).then(res => res.text()).then(text => {
                console.log(text);
            });
        },
        async getKeyframes() {
            let result = await fetch(`${this.apiUrl}/api/session/${this.sessionId}/keyframes`).then(res => res.json());
            this.pages.p1.frames = result.frames;
        },
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
