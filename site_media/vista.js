$(document).ready(function(){
    $("input:image").click(function() {
        var dataString = 'id='+ this.id;
        $.ajax({
            type: "GET",
            url: "http://localhost:8000/peliculas/vista/",
            data: dataString
        });
        var src = this.src;
        if(src.match("ok")=="ok"){
            src = $(this).attr("src").replace("ok", "cancel");
            $(this).attr("src", src);
        }else{
            src = $(this).attr("src").replace("cancel", "ok");
            $(this).attr("src", src);
        }
        return false;
    });
});