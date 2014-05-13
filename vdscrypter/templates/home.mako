<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>VDScrypter - Choose Folder</title>
  </head>

  <body id="main_body" >
  <div style="text-align:center;">
    <img src="static/images/All-seeing-Eye-852x754.jpg"/>

	<div id="form_container" style="width:200px;margin:0 auto;text-align:left;">
        <form id="folder_select" class="appnitro"  method="post" action="/folder">
					<div class="form_description">
		</div>
			<ul >
					<li id="li_1" >
		<label class="description" for="folder_path">Absolute path to images: </label>
		<div>
			<input id="folder_path" name="folder_path" class="element text large" type="text" maxlength="255" value=""/>
		</div
		</li>		<li id="li_2" >
		<label class="description" for="recurse"></label>
		<span>
			<input id="recurse" name="recurse" class="element checkbox" type="checkbox" value="1" />
        <label class="choice" for="recurse">Recurse subfolders</label>

		</span>
		</li>

					<li class="buttons">
			    <input type="hidden" name="form_id" value="submit_folder" />

				<input id="saveForm" class="button_text" type="submit" name="submit" value="Submit" />
		</li>
			</ul>
		</form>
	</div>
  </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
  </body>
</html>
