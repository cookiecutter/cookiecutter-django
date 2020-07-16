import axios from "axios";

// axios settings
axios.defaults.baseURL = process.env.VUE_APP_API_ROOT;
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'csrftoken';


const api = axios.create({});


export default {
{%- if cookiecutter.use_fruit_demo == "y" %}
    getFruits: function () {
        return api.get('/fruits/')
    },
    getFruit: function (id) {
        return api.get('/fruits/' + id + '/')
    }
{%- endif %}
    /* Include additional API calls here */
}

