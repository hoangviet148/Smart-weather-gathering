// Import the dependencies and necessary modules
import Vue from 'vue';
import App from './App.vue';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import Widgets from 'fusioncharts/fusioncharts.widgets';
import PowerCharts from 'fusioncharts/fusioncharts.powercharts';
import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
import VueFusionCharts from 'vue-fusioncharts';
import VueSocketIO from "vue-socket.io";

// Resolve the dependencies
Charts(FusionCharts);
PowerCharts(FusionCharts);
Widgets(FusionCharts);
FusionTheme(FusionCharts);

// Globally register the components for project-wide use
Vue.use(VueFusionCharts, FusionCharts);

Vue.use(new VueSocketIO({
  debug: true,
  connection: 'http://192.168.1.163:3000',
}))

// Instantiate the Vue instance that controls the application
new Vue({
  el: '#app',
  render: h => h(App)
})
