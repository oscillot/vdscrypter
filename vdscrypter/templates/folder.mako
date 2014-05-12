<!DOCTYPE html>
<html lang="${request.locale_name}">
<head>
    <title>VDScrypter - Choose Options</title>
</head>

<body>
    %for i, f in enumerate(found):
        <div id="form_container_${i}" style="white-space: nowrap;">
            <img src="${f[0]}" style="height:225px;max-width:400px;width: expression(this.width > 400 ? 400: true);"/>
            <div style="display: inline-block; vertical-align: top;">

            <form id="form_${i}" method="post" action="javascript:preview(${i}); return false;">
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
##                            <small>How many times to loop the video</small>
                        </p>
                    </li>
                    <li id="li_3_${i}">
                        <label class="description" for="element_3">Bounce </label>
		                <span>
			                <input id="bounce_${i}" name="bounce_${i}" class="element checkbox " type="checkbox"/>
                            <label class="choice" for="bounce_${i}">Enable</label>
		                </span>
                        <p class="guidelines" id="guide_3_${i}">
##                            <small>Bounce plays the asset once forwards and once in reverse. This has an implicit loop.</small>
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
##                            <small>Whether to stretch or to letterbox for the resize that must occur.</small>
                        </p>
                    </li>

                    <li>
                        <label class="description" for="element_4">FPS</label>
                        <span>
			                <input id="fps_${i}" name="fps_${i}" class="element" type="text" maxlength="255" value="30"/>
                            <label class="choice" for="fps_${i}">Enable</label>
		                </span>
                        <p class="guidelines" id="guide_4_${i}">
##                            <small>How many frames to play per second. May need to tweak on a per-gif basis.</small>
                        </p>
                    </li>
                    <li class="buttons">
                        <input type="hidden" name="form_id" value="preview_${i}"/>
                        <input id="saveForm_${i}" class="button_text" type="submit" name="submit" value="Preview"/>
                    </li>
                </ul>
            </form>
            <div id="footer_${i}" style="display: none;"></a>
            </div>
            </div>
        </div>
    %endfor

<script>
function preview(i){
    console.log(i);
    var full_path = $("#full_path_" + i + "").val();
    var loop = $("#loop_" + i + "").is(":checked");
    var repeat = $("#repeat_" + i + "").val();
    var bounce = $("#bounce_" + i + "").is(":checked");
    var fps = $("#fps_" + i + "").val();
    var resize = $("input[type='radio'][name='resize_" + i + "']:checked").val();
    $.ajax({
        type: "POST",
        url: "/preview",
        data: {full_path: full_path,
               loop: loop,
               repeat: repeat,
               bounce: bounce,
               fps: fps,
               resize: resize
        },
        dataType:'json'
    });
}
</script>

<script src="static/js/h5utils.js"></script>
<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
</body>
</html>
