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
                    <i>▲</i>
                    {{ currentWeather.todayHighLow.todayTempHigh }}
                    <span>°C</span>
                  </div>
                  <div id="max-summary">
                    at {{ currentWeather.todayHighLow.todayTempHighTime }}
                  </div>
                </div>
                <div class="min-desc">
                  <div id="min-detail">
                    <i>▼</i>
                    {{ currentWeather.todayHighLow.todayTempLow }}
                    <span>°C</span>
                  </div>
                  <div id="min-summary">
                    at {{ currentWeather.todayHighLow.todayTempLowTime }}
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
      this.currentWeather.summary = data.conclusion
      this.highlights.uvIndex = data.uv
      this.highlights.humidity = data.humid
      this.highlights.pressure = data.pressure
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
        temp: "N/A",
        todayHighLow: {
          todayTempHigh: "1",
          todayTempHighTime: "1:00 PM",
          todayTempLow: "1",
          todayTempLowTime: "1:00 PM",
        },
        summary: "cal...",
        possibility: "",
      },
      tempVar: {
        tempToday: [
          // gets added dynamically by this.getSetHourlyTempInfoToday()
          {"hour": 1, "temp": 1}, {"hour": 2, "temp": 3}
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

    async getCurrentTemp() {
      //var currentTemp = this.rawWeatherData.currently.temperature;
      //this.currentWeather.temp = this.fahToCel(currentTemp);
      //this.currentWeather.temp = 1;
    },

    organizeCurrentWeatherInfo() {
      this.getCurrentTime();
      this.getCurrentTemp();
    },

    // topmost level orchestration
    organizeAllDetails() {
      // top level organization
      var self = this;
      self.getCoordinates();
      this.organizeCurrentWeatherInfo();
      //this.organizeTodayHighlights();
      //this.getSetHourlyTempInfoToday();
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
