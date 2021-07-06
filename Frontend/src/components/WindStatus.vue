<template>
  <div class="highlights-item col-md-4 col-sm-6 col-xs-12 border-top">
    <div>
      <div class="card-heading pt-5">Humidity</div>
      <div class="row pt-4 mt-4">
        <div class="col-sm-6 col-md-6 mt-2 text-center align-middle">
          <p class="card-sub-heading mt-3" style="color: white">
            Wind Direction
          </p>
          <!-- <p class="mt-4"><img src="../assets/winddirection.svg" height="40" width="40"></p> -->
          <p class="mt-2 ml-12" style="font-size: 30px">
            {{ highlights.humidity }}
          </p>
        </div>
        <div class="col-sm-6 col-md-6 mt-2">
          <!-- <p class="card-sub-heading mt-3">Wind Speed</p> -->
          <p class="mt-4 mr-7">
            <img src="../assets/humidity.svg" height="100" width="100" />
          </p>
          <p class="mt-4">{{ highlights.windStatus.windSpeed }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["highlights"],
  data() {
    return {};
  },
  methods: {},
  computed: {},
};
</script>

<style>
</style>
