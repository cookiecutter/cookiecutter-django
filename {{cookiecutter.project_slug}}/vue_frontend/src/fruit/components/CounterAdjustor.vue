<template>
    <div>

        <!-- Because project css is loaded on our base tempalte, we can use those styles -->
        <div class="btn-group" role="group">
            <button v-if="this.showDecrement()" class="btn btn-outline-primary" @click="decrement">-</button>
            <button v-if="this.showIncrement()" class="btn btn-outline-primary" @click="increment">+</button>
        </div>


    </div>
</template>

<script>
    import {ACTION_DECREMENT_COUNTER, ACTION_INCREMENT_COUNTER} from "../store/module_fruit";

    export default {
        name: 'CounterAdjustor',
        props: {
            mode: {
                type: String,
                default: 'all'
            }
        },
        methods: {
            showDecrement() {
                return this.mode === 'dec' || this.mode === 'all'
            },
            showIncrement() {
                return this.mode === 'inc' || this.mode === 'all'
            },
            increment() {
                this.$store.dispatch(ACTION_INCREMENT_COUNTER)
            },
            decrement() {
                this.$store.dispatch(ACTION_DECREMENT_COUNTER)
            }
        },
    }
</script>

<style scoped lang="scss">

    button {
        font-size: 2rem;
        line-height: 2rem;
        font-weight: bold;
        width: 3rem;
        height: 3rem;
        color: #5a5a5a;
        border-color: #5a5a5a;
    }


</style>
