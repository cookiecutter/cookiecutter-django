<template>
  <div>
    <p class="">{% raw %}{{ message }}{% endraw %}</p>
  </div>
</template>

<script>
  export default {
    name: 'CounterBanner',
    props: { },
    computed: {
      count() { return this.$store.state.fruit.count },
      message() { 
        if (this.count <= 3) {
          return "You like fruit, don't you?";
        } else if (this.count <= 6) {
          return "Just right.";
        } else if (this.count <= 12) {
            return "You must be hungry!";
        } else {
          return "You must be very hungry!";
        }
      }
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  p {
    font-style: italic;
    font-size: 2rem;
  }
</style>