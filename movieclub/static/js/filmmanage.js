


/*
function deleteconfirm(){
    var r = confirm("Confirmación de eliminación");
    if (r == true) {
        //Eliminar;
    } else {
        //No hacer nada;
    }
}
*/




$(document).ready(function(){

$('.delbtn').click(function(){

    var cont = $(this).attr('id');

    $('#alert' + cont).fadeIn();

    $('.cancel').click(function(){
        $(this).parent().fadeOut();
    });

});











});