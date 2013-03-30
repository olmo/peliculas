$(document).ready(function(){
    $("input:checkbox").click(function() {
        var dataString = 'id='+ this.id;
        $.ajax({
            type: "GET",
            url: "http://1984.dyndns.org/peliculas/peliculas/vista/",
            data: dataString
        });
        return false;
    });

    var tooltipvalues = ['basura', 'mala', 'normal', 'buena', 'excelente'];
    $('.rateit').bind('rated reset', function (event, value) {
        var ri = $(this);
        $(this).attr('title', tooltipvalues[value-1]);

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