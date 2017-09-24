$(function() {

  /**
 * Copyright (c) 2011-2014 Felix Gnass
 * Licensed under the MIT license
 * http://spin.js.org/
 */

  $.fn.spin = function(opts, color) {

    return this.each(function() {
      var $this = $(this)
        , data = $this.data()

      if (data.spinner) {
        data.spinner.stop()
        delete data.spinner
      }
      if (opts !== false) {
        opts = $.extend(
          { color: color || $this.css('color') }
        , $.fn.spin.presets[opts] || opts
        )
        data.spinner = new Spinner(opts).spin(this)
      }
    })
  }

  $.fn.spin.presets = {
    tiny:  { lines:  8, length: 2, width: 2, radius: 3 }
  , small: { lines:  8, length: 4, width: 3, radius: 5 }
  , large: { lines: 10, length: 8, width: 4, radius: 8 }
  }

  /* spinner end */

  $('#submit-btn').on('click', function(){
    $('#main').spin();
    const fd = new FormData(document.querySelector("form"));
    $("#upload-warning").hide();
    $("#message").text("Uploading and processing file...");
    $("#message").show();
    // const spinner = new Spinner().spin();
    $.ajax({
      url: "/upload_file",
      type: "POST",
      data: fd,
      processData: false,  // tell jQuery not to process the data
      contentType: false,  // tell jQuery not to set contentType
      success: function() {
        $("#message").text("File uploaded successfully!");
        $("#message").show();
        $('#main').spin(false);
        $("#upload-info").hide();
      },
      error: function() {
        $("#message").text("Sorry, there was an error. Please check you have uploaded a file that exists and try again.");
        $("#message").show();
        $('#main').spin(false);
      },
    });
   return false;
  });

  $('#query').submit(function(event) {
    $('#main').spin();
    event.preventDefault();
    const query = $(this).serialize();
    $.ajax({
      url: "/item?" + query,
      type: "GET",
      success: function(res) {
        if ($.isEmptyObject(res)){
          $("#query-result").text("Object did not exist at that time.");
          $("#query-result").show();
        } else {
          let result_text = "<h5>Query result</h5>"
          for (let key in res) {
            let value = res[key];
            result_text += `<b>${key}</b>: ${value}<br/>`
          }
          $("#query-result").html(result_text);
          $("#query-result").show();
        }
        $('#main').spin(false);
        return false;
      },
      error: function() {
        $('#main').spin(false);
      }
    })
  })

});