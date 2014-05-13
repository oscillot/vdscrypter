<%!
    import os
    %>
<!DOCTYPE html>
<html lang="${request.locale_name}">
<head>
    <title>VDScrypter - Choose Options</title>
</head>

<body>
            <form id="fps_form" method="post" action="javascript:void(0);">
                FPS: <input id="fps" name="fps" type="text" maxlength="255" value="15"/> This value is GLOBAL!
                <input id="fps_hidden" style="display:none;" class="button_text" type="submit" name="hidden" value="hidden"/>
                <ul>
                    <li>
                        <div>
                            <label class="description">Global Loop</label>
                            <label class="choice">Enable looping</label>
                            <input id="loop_global" name="loop_global" class="element checkbox" type="checkbox" onchange="setLoops();"/>
                        </div>
                        <div>
                            <label class="description">Global Loop Count </label>
                            <input id="repeat_global" name="repeat_global" class="element text small" type="text" maxlength="255" value="1" onchange="setRepeat();"/>
                        </div>
                    </li>
                    <br>
                    <li>
                        <div>
                            <label class="description">Global Reverse</label>
                            <input id="reverse_global" name="reverse_global" class="element checkbox " type="checkbox"  onchange="setReverse();"/>
                        </div>
                    </li>
                    <br>
                    <li>
                        <div>
                            <label class="description">Global Bounce</label>
                            <input id="bounce_global" name="bounce_global" class="element checkbox " type="checkbox"  onchange="setBounce();"/>
                        </div>
                    </li>
                    <br>
                    <li>
                        <div>
                            <label>Global Resize technique</label>
                            <input name="resize_global" class="resize_global" type="radio" value="fill" checked="1" onchange="setResize();">Fill
                            <input name="resize_global" class="resize_global" type="radio" value="box" onchange="setResize();">Box
                            <label class="choice" for="resize_global"></label>
		                </div>
                    </li>
                    <br>
                </ul>
            </form>
    <div id="outer_sort">
    %for i, f in enumerate(found):
        <div id="form_container_${i}" style="white-space: nowrap;position: relative;" class="sortable">
            <h3>${f[1].rsplit(os.path.sep, 1)[1]}</h3>
            <img src="${f[0]}" style="height:225px;max-width:400px;width: expression(this.width > 400 ? 400: true);" class="img_cls"/>
            <div style="display: inline-block; vertical-align: top;">

            <form id="form_${i}" method="post" action="javascript:preview(${i}, true, true);" class="preview_form">
                <input id="full_path_${i}" name="full_path_${i}" class="element" type="text" value="${f[1]}" style="display:none;"/>
                <ul>
                    <li>
                        <div>
                            <label class="description">Loop</label>
                            <label class="choice">Enable looping</label>
                            <input id="loop_${i}" name="loop_${i}" class="element checkbox loop" type="checkbox"/>
                        </div>
                        <div>
                            <label class="description">Loop Count </label>
                            <input id="repeat_${i}" name="repeat_${i}" class="element text small repeat" type="text" maxlength="255" value="1"/>
                        </div>
                    </li>
                    <br>
                    <li>
                        <div>
                            <label class="description">Reverse</label>
                            <input id="reverse_${i}" name="reverse_${i}" class="element checkbox reverse" type="checkbox"/>
                        </div>
                    </li>
                    <br>
                    <li>
                        <div>
                            <label class="description">Bounce</label>
                            <input id="bounce_${i}" name="bounce_${i}" class="element checkbox bounce" type="checkbox"/>
                        </div>
                    </li>
                    <br>
                    <li>
                        <div>
                            <label>Resize technique</label>
                            <input name="resize_${i}" class="element resize" type="radio" value="fill" checked="1">Fill
                            <input name="resize_${i}" class="element resize" type="radio" value="box">Box
                            <label class="choice" for="resize_${i}"></label>
		                </div>
                    </li>
                    <br>
                    <li>
                    <div>
                        <input type="hidden" name="form_id" value="preview_${i}"/>
                        <input id="saveForm_${i}" class="button_text" type="submit" name="submit" value="Preview"/>
                    </div>

                    <div>
                        <input id="delete_${i}" class="button_text" style="float:right;" type="submit" name="delete" value="Delete?" onclick="deleteMe(${i});"/>
                    </div>
                    </li>
                </ul>
            </form>
        </div>
    </div>
    %endfor
        <br>
            <form id="render_form" method="post" action="javascript:render();">
                Output folder: <input id="output" name= "output" type="text" maxlength="2048" value=""/> (leave blank to save at the root).
                <input id="compress" name="compress" class="element checkbox " type="checkbox" checked="1"/>Compress with Xvid? (You probably want this.)
                <input id="render" class="button_text" type="submit" name="Render" value="Render"/>
            </form>
    </div>
    <div>
        <h3 id="gotmade" style="color:green;"></h3>
    </div>
    <div id="floor" style="display:hidden"></div>

<script>
var count = ${len(found)};
var rendered = [];

function setLoops(){
    var global_loop = $("#loop_global");
    var loops = $(".loop");
    if (global_loop.is(':checked')){
        for (var i=0;i<loops.length;i++){
            loops[i].checked = true;
        }
    } else {
        for (var j=0;j<loops.length;j++){
            loops[j].checked = false;
            }
        }
    }


function setRepeat(){
    var global_repeat = $("#repeat_global");
    var repeats = $(".repeat");
    for (var i=0;i<repeats.length;i++){
        repeats[i].value = global_repeat.val();
    }
}

function setReverse(){
    var global_reverse = $("#reverse_global");
    var reversed = $(".reverse");
    if (global_reverse.is(':checked')){
        for (var i=0;i<reversed.length;i++){
            reversed[i].checked = true;
        }
    } else {
        for (var j=0;j<reversed.length;j++){
            reversed[j].checked = false;
            }
        }
    }

function setBounce(){
    var global_bounce = $("#bounce_global");
    var bounces = $(".bounce");
    if (global_bounce.is(':checked')){
        for (var i=0;i<bounces.length;i++){
            bounces[i].checked = true;
        }
    } else {
        for (var j=0;j<bounces.length;j++){
            bounces[j].checked = false;
            }
        }
    }

function setResize(){
    var global_resize = $(".resize_global");
    for (var i=0;i<global_resize.length;i++){
        if (global_resize[i].checked == true){
            var method = global_resize[i].value;
        }
    }
    var resizes = $(".resize");
    for (var j=0;j<resizes.length;j++){
        if (resizes[j].value == method){
            resizes[j].checked = true;
        } else {
            resizes[j].checked = false;
        }
    }
}

function deleteMe(i){
    var confirmation = confirm("Sure to delete?");
    if (confirmation == true){
        $("#form_container_" + i + "").remove();
    }
}

function returnJson(data, status, xhr){
    console.log(data);
    rendered.push(data.rendered);
}

function logError(error, xhr){
    console.log(error);
    return null
}

function preview(i, preview, async){
##    console.log(i);
    var repeat = $("#repeat_" + i + "").val();
    if (repeat < 1 || repeat > 32){
        alert('Invalid: Must be one of 1-32');
        return false;
    }
    var fps = $("#fps").val();
    if (fps < 1 || fps > 300){
        alert('Invalid: Must be one of 1-300');
        return false;
    }
    var full_path = $("#full_path_" + i + "").val();
    var loop = $("#loop_" + i + "").is(":checked");
    var bounce = $("#bounce_" + i + "").is(":checked");
    var reverse = $("#reverse_" + i + "").is(":checked");
    var resize = $("input[type='radio'][name='resize_" + i + "']:checked").val();
    $.ajax({
        type: "POST",
        url: "/preview",
        data: {full_path: full_path,
               loop: loop,
               repeat: repeat,
               bounce: bounce,
               reverse: reverse,
               fps: fps,
               resize: resize,
               preview: preview
        },
        dataType:'json',
        success: returnJson,
        error: logError,
        async: async
    });
}

function printData(data, status, xhr){
    console.log(data);
}

function alertSavePath(data, status, xhr){
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:6543/cleanup"
    });
##    alert("File was rendered to: " + data.output);
    $('#gotmade').text("File was rendered to: " + data.output);
    $('#floor')[0].scrollIntoView();
}

function render(){
##    reset renders in case previews has populated it at all
    rendered = [];
##    if (rendered.length == 0){
##        alert("ERROR! Need at least 1 item in the render pipeline!");
##        return;
##    }
    var forms = $(".preview_form");
    var compress = $("#compress").is(":checked");
    var fps = $('#fps').val();
    if (parseInt(fps) < 1 || parseInt(fps > 300)){
        alert('Invalid: Must be one of 1-300');
        return false;
    }
    var output = $('#output').val();

    console.log(forms);
    for (var i=0;i<forms.length;i++){
        var raw_id = forms[i].attributes['id'].value.substring('form_'.length);
        preview(raw_id, false, false);
    }
    $.ajax({
        type: "POST",
        url: "/render",
        data: {rendered: rendered,
               folder_path: "${folder_path.replace('\\', '\\\\')}",
               output: output,
               compress: compress},
        dataType:'json',
        success: alertSavePath,
        error: logError
    });
}

</script>

<script src="static/js/h5utils.js"></script>
<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
<script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>

<script>
$(document).ready(function(){
    $('#outer_sort').sortable({placeholder: "ui-state-highlight",helper:'clone'});
})
</script>

</body>
</html>
