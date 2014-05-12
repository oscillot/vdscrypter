<!DOCTYPE html>
<html lang="${request.locale_name}">
<head>
    <title>VDScrypter - Choose Options</title>
</head>

<body>
            <form id="fps_form" method="post" action="javascript:void(0);">
                FPS: <input id="fps" name="fps" type="text" maxlength="255" value="30"/> This value is GLOBAL!
                <input id="fps_hidden" style="display:none;" class="button_text" type="submit" name="hidden" value="hidden"/>
            </form>
    <div id="outer_sort">
    %for i, f in enumerate(found):
        <div id="form_container_${i}" style="white-space: nowrap;position: relative;" class="sortable">
            <img src="${f[0]}" style="height:225px;max-width:400px;width: expression(this.width > 400 ? 400: true);" class="img_cls"/>
            <div style="display: inline-block; vertical-align: top;">

            <form id="form_${i}" method="post" action="javascript:preview(${i}, true, true);" class="preview_form">
                <input id="full_path_${i}" name="full_path_${i}" class="element" type="text" value="${f[1]}" style="display:none;"/>
                <ul>
                    <li id="li_2_${i}">
                        <label class="description" for="element_2"></label>
		                <span>
			                <input id="loop_${i}" name="loop_${i}" class="element checkbox" type="checkbox"/>
                            <label class="choice" for="loop_${i}">Enable looping</label>
                        </span>
                    </li>
                    <li id="li_1">
                        <label class="description" for="repeat_${i}">Loop Count </label>
                        <div>
                            <input id="repeat_${i}" name="repeat_${i}" class="element text small" type="text" maxlength="255" value="1"/>
                        </div>
                        <p class="guidelines" id="guide_1_${i}">
                        </p>
                    </li>
                    <li id="li_3_${i}">
                        <label class="description" for="element_3">Bounce </label>
		                <span>
			                <input id="bounce_${i}" name="bounce_${i}" class="element checkbox " type="checkbox"/>
                            <label class="choice" for="bounce_${i}">Enable</label>
		                </span>
                        <p class="guidelines" id="guide_3_${i}">
                        </p>
                    </li>

                    <li>
                        <label class="resize_${i}" for="element_5">Resize technique</label>
                        <span>
			                <input name="resize_${i}" class="element" type="radio" value="box" checked="1">Box
			                <input name="resize_${i}" class="element" type="radio" value="fill">Fill
                            <label class="choice" for="resize_${i}"></label>
		                </span>
                        <p class="guidelines" id="guide_5_${i}">
                        </p>
                    </li>
                    <li class="buttons">
                        <input type="hidden" name="form_id" value="preview_${i}"/>
                        <input id="saveForm_${i}" class="button_text" type="submit" name="submit" value="Preview"/>
                    </li>
                </ul>
            </form>
        </div>
    </div>
    %endfor
            <form id="render_form" method="post" action="javascript:render();">
                Output folder: <input id="output" name= "output" type="text" maxlength="2048" value=""/> (leave blank to save at the root).
                <input id="render" class="button_text" type="submit" name="Render" value="Render"/>
            </form>
    </div>

<script>
var count = ${len(found)};
var rendered = [];

function returnJson(data, status, xhr){
    console.log(data);
    rendered.push(data.rendered);
}

function logError(error, xhr){
    console.log(error);
    return null
}

function preview(i, preview, async){
    console.log(i);
    var full_path = $("#full_path_" + i + "").val();
    var loop = $("#loop_" + i + "").is(":checked");
    var repeat = $("#repeat_" + i + "").val();
    var bounce = $("#bounce_" + i + "").is(":checked");
    var fps = $("#fps").val();
    var resize = $("input[type='radio'][name='resize_" + i + "']:checked").val();
    $.ajax({
        type: "POST",
        url: "/preview",
        data: {full_path: full_path,
               loop: loop,
               repeat: repeat,
               bounce: bounce,
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
    alert("File was rendered to: " + data.output);
}

function render(){
##    reset renders in case previews has populated it at all
    rendered = [];
    var forms = $(".preview_form");
    var fps = $('#fps').val();
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
               output: output},
        dataType:'json',
        success: alertSavePath,
        error: logError,
        async: true
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
