<template>
  <div id="ancestor">
    <div class="container-fluid" id="app">
      <div class="row">
        <div id="sidebar" class="col-md-3 col-sm-4 col-xs-12 sidebar">
          <div id="info">
            <div class="wrapper-left">
              <div id="current-weather">
                {{ currentWeather.temp }}
                <span>°C</span>
              </div>
              <div id="weather-desc">{{ currentWeather.summary }}</div>
              <div class="temp-max-min">
                <div class="max-desc">
                  <div id="max-detail">
                    <i id="1h">▲</i>
                    {{ currentWeather.futureTemp.temp1 }}
                    <span>°C</span>
                  </div>
                  <div id="max-summary">
                    at {{ currentWeather.futureTemp.time1 }}
                  </div>
                </div>
                <div class="min-desc">
                  <div id="min-detail">
                    <i id="4h">▼</i>
                    {{ currentWeather.futureTemp.temp4 }}
                    <span>°C</span>
                  </div>
                  <div id="min-summary">
                    at {{ currentWeather.futureTemp.time4 }}
                  </div>
                </div>
              </div>
            </div>
            <div class="wrapper-right">
              <div class="date-time-info">
                <div id="date-desc">
                  <img src="./assets/calendar.svg" width="20" height="20" />
                  {{ currentWeather.time }}
                </div>
              </div>
              <div class="location-info">
                <div id="location-desc">
                  <img
                    src="./assets/location.svg"
                    width="10.83"
                    height="15.83"
                    style="opacity: 0.9"
                  />
                  {{ currentWeather.full_location }}
                  <div id="location-detail" class="mt-1">
                    Lat: {{ currentWeather.formatted_lat }}
                    <br />
                    Long: {{ currentWeather.formatted_long }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <dashboard-content
          class="col-md-9 col-sm-8 col-xs-12 content"
          id="dashboard-content"
          :highlights="highlights"
          :tempVar="tempVar"
        ></dashboard-content>
      </div>
    </div>
  </div>
</template>

<script>
import Content from "./components/Content.vue";
import axios from "axios";

export default {
  name: "app",
  components: {
    "dashboard-content": Content,
  },

  sockets: {
    connect() {
      console.log("socket connected");
    },
    UpdateData(data) {
      this.currentWeather.temp = data.curTemp;
      this.currentWeather.summary = data.conclusion;
      this.highlights.uvIndex = data.uv;
      this.highlights.humidity = data.humid;
      this.highlights.pressure = data.pressure;
      // console.log("this method was fired by the socket server: ", data);
    },
    UpdateFutureTempPrediction(data) {
      console.log("=====alo=====");
      console.log("this method was fired by the socket server: ", data);
    },
  },

  data() {
    return {
      weatherDetails: false,
      location: "",
      lat: "", // raw latitude from google maps api response
      long: "", // raw longitude from google maps api response
      completeWeatherApi: "", // weather api string with lat and long
      rawWeatherData: "", // raw response from weather api
      currentWeather: {
        full_location: "", // for full address
        formatted_lat: "", // for N/S
        formatted_long: "", // for E/W
        time: "",
        temp: "-",
        futureTemp: {
          temp1: "-",
          time1: "-:- PM",
          temp4: "-",
          time4: "-:- PM",
        },
        summary: "-",
        possibility: "",
      },
      tempVar: {
        tempToday: [
          // gets added dynamically by this.getSetHourlyTempInfoToday()
          { "hour": "0", temp: 26 },
          { hour: "1", temp: 27 },
          { hour: "2", temp: 27 },
          { hour: "3", temp: 27.4 },
          { hour: "4", temp: 27.5 },
          { hour: "5", temp: 28.2 },
          { hour: "6", temp: 29 },
          { hour: "7", temp: 29 },
          { hour: "8", temp: 29.8 },
          { hour: "9", temp: 30.2 }
        ],
      },
      highlights: {
        uvIndex: "",
        visibility: "",
        humidity: "",
        pressure: "",
        windStatus: {
          windSpeed: "",
          windDirection: "",
          derivedWindDirection: "",
        },
      },
    };
  },
  methods: {
    // Some utility functions
    convertToTitleCase(str) {
      str = str.toLowerCase().split(" ");
      for (var i = 0; i < str.length; i++) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
      }
      return str.join(" ");
    },
    formatPossibility(str) {
      str = str.toLowerCase().split("-");
      for (var i = 0; i < str.length; i++) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
      }
      return str.join(" ");
    },
    fahToCel: function (tempInFahrenheit) {
      var tempInCelcius = Math.round((5 / 9) * (tempInFahrenheit - 32));
      return tempInCelcius;
    },
    milibarToKiloPascal(pressureInMilibar) {
      var pressureInKPA = pressureInMilibar * 0.1;
      return Math.round(pressureInKPA);
    },
    mileToKilometer: function (miles) {
      var kilometer = miles * 1.60934;
      return Math.round(kilometer);
    },

    //  Some basic action oriented functions
    makeTempVarTodayEmpty() {
      this.tempVar.tempToday = [];
    },

    locationEntered() {
      this.makeTempVarTodayEmpty();
    },

    async getCoordinates() {
      var self = this;
      let lat, long;

      await navigator.geolocation.getCurrentPosition(async (position) => {
        lat = await position.coords.latitude;
        long = await position.coords.longitude;
        self.currentWeather.formatted_lat = lat;
        self.currentWeather.formatted_long = long;
      });

      self.currentWeather.full_location = "Hanoi, Vietnam";
    },

    getCurrentTime() {
      this.currentWeather.time = new Date().toString().slice(0, 21);
    },

    async predictFutureTemp() {
      console.log("alo")
      let response1 = await axios.get(
        "http://192.168.1.163:3000/api/getFutureTemp1"
      );
      let response4 = await axios.get(
        "http://192.168.1.163:3000/api/getFutureTemp4"
      );

      let temp1 = response1.data - parseFloat(this.currentWeather.temp);
      let temp4 = response4.data - parseFloat(this.currentWeather.temp);
      if (temp1 > 0) {
        document.getElementById("1h").innerHTML = "▲";
      } else {
        document.getElementById("1h").innerHTML = "▼";
      }
      if (temp4 > 0) {
        document.getElementById("4h").innerHTML = "▲";
      } else {
        document.getElementById("4h").innerHTML = "▼";
      }
      this.currentWeather.futureTemp.temp1 = Math.abs(temp1.toFixed(1));
      this.currentWeather.futureTemp.temp4 = Math.abs(temp4.toFixed(1));

      let d = new Date();
      let hours = d.getHours();
      let ampm = hours >= 12 ? "PM" : "AM";
      this.currentWeather.futureTemp.time1 = String(hours + 2) + ":00 " + ampm;
      this.currentWeather.futureTemp.time4 = String(hours + 4) + ":00 " + ampm;
    },

    organizeCurrentWeatherInfo() {
      this.getCurrentTime();
      setTimeout(() => {
        this.predictFutureTemp();
      }, 3000);
    },

    async getSetTempChart() {
      let res = await axios.get("http://192.168.1.163:3000/api/getChartData");
      let chartData = res.data.chartData;

      for (let i = 0; i < chartData.length; i++) {
        this.tempVar.tempToday.push(chartData[i]);
      }
    },

    organizeAllDetails() {
      var self = this;
      self.getCoordinates();
      this.organizeCurrentWeatherInfo();
      // this.getSetTempChart();
    },
  },

  mounted() {
    var self = this;
    this.location = "Ha Noi";
    self.organizeAllDetails();
  },
};
</script>

<style lang="scss">
</style>
