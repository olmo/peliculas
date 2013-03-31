function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    $("input:checkbox").click(function() {
        $(this).prop('checked', !this.checked);
        $.ajax({
            type: "POST",
            url: "http://1984.dyndns.org/peliculas/peliculas/vista/",
            data: { id: this.id }
            /*context: this,
            success: function (data) {
                $(this).prop('checked', !this.checked);
            }*/
        });
        return false;
    });

    var tooltipvalues = ['basura', 'mala', 'normal', 'buena', 'excelente'];
    $(".rateit").bind('over', function (event, value) { $(this).attr('title', tooltipvalues[value-1]); });

    $('.rateit').bind('rated reset', function (e) {
        var ri = $(this);

        var value = ri.rateit('value');
        var peliculaID = ri.data('peliculaid');

        //ri.rateit('readonly', true);

        $.ajax({
            url: 'http://1984.dyndns.org/peliculas/peliculas/votar/',
            data: { id: peliculaID, value: value },
            type: 'POST'
        });
    });
});