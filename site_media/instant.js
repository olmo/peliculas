$(document).ready(function(){
	var runningRequest = false;
	var request;
    
	$('input#q').keyup(function(e){
		e.preventDefault();
		var $q = $(this);

		if($q.val() == ''){
			$('div#results').html('');
			return false;
		}
		
		if(runningRequest){
			request.abort();
		}

		runningRequest=true;
		request = $.getJSON('/listas/busqueda_ajax',{
			q:$q.val()
		},function(data){
			showResults(data,$q.val());
			runningRequest=false;
		});
		
		function showResults(data, highlight){
		   var resultHtml = '<ul class="steps">';
			$.each(data, function(i,item){
				resultHtml+='<li id="'+item.id+'">';
                resultHtml+='<img src="/site_media/posters/'+item.poster+'" width="50" />';
				resultHtml+='<h5>'+item.titulo+'</h5>';
                resultHtml+='<p>'+item.titulo+'</p>';
				resultHtml+='</li>';
			});
            resultHtml+='</ul>';

			$('div#results').html(resultHtml);

            $( "#results li" ).draggable({
                cancel: "a.ui-icon", // clicking an icon won't initiate dragging
                revert: "invalid", // when not dropped, the item will revert back to its initial position
                containment: $( "#demo-frame" ).length ? "#demo-frame" : "document", // stick to demo-frame if present
                helper: "clone",
                cursor: "move"
            });
		}

		$('form').submit(function(e){
			e.preventDefault();
		});
	});




    var $gallery = $( "#gallery" ),
		$lista = $( "#lista" );
    var $obj, $l;

    $( "#results li" ).draggable({
        cancel: "a.ui-icon", // clicking an icon won't initiate dragging
        revert: "invalid", // when not dropped, the item will revert back to its initial position
        containment: $( "#contenedor" ).length ? "#contenedor" : "document", // stick to demo-frame if present
        helper: "clone",
        cursor: "move",
        connectToSortable: '#sortable'
    });

    $('#lista ul').sortable();
    
    $("#lista").droppable({
        accept: "#results li",
        activeClass: "ui-state-highlight",
        drop: function( event, ui ) {
            $obj = ui.draggable.attr('id');
            $l = $('#contenido h2').attr('id');
            request = $.getJSON('/listas/add_elemento',{
                obj:$obj,l:$l
            });

            agregarImagen( ui.draggable );
        }
    });

    $("#results").droppable({
        accept: "#trash li",
        activeClass: "custom-state-active",
        drop: function( event, ui ) {
            eliminarImagen( ui.draggable );
        }
    });
    
    function agregarImagen( $item ) {
        $item.fadeOut(function() {
            var $list = $( "ul", $lista ).length ?
                $( "ul", $lista ) :
                $( "<ul class='gallery ui-helper-reset'/>" ).appendTo( $lista );
            
            $item.appendTo( $list ).fadeIn(function() {
                $item
                    .animate({ width: "48px" })
                    .find( "img" )
                        .animate({ height: "36px" });
            });
        });
    }
    
    function eliminarImagen( $item ) {
        $item.fadeOut(function() {
            $item
                .find( "a.ui-icon-refresh" )
                    .remove()
                .end()
                .css( "width", "96px")
                .append( trash_icon )
                .find( "img" )
                    .css( "height", "72px" )
                .end()
                .appendTo( $gallery )
                .fadeIn();
        });
    }
});