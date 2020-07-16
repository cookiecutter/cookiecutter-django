{%- if cookiecutter.use_vue == 'y' %}
function load_bundle_file(url, filetype) {
    let fileref;
    if (filetype === "js") { // build js script tag
        fileref = document.createElement('script');
        fileref.setAttribute("type", "text/javascript");
        fileref.setAttribute("src", url);
    } else if (filetype === "css") { // build css link tag
        fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", url);
    }
    if (typeof fileref != "undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref);
}

{% endif -%}
/* Project specific Javascript goes here. */
