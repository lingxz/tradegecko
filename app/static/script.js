$(function() {
  $('#submit-btn').on('click', function(){
   const fd = new FormData(document.querySelector("form"));
   $("#upload-warning").hide();
   $("#message").text("Uploading and processing file...");
   $("#message").show();
   $.ajax({
      url: "/upload_file",
      type: "POST",
      data: fd,
      processData: false,  // tell jQuery not to process the data
      contentType: false,  // tell jQuery not to set contentType
      success: function() {
        $("#message").text("File uploaded successfully!");
        $("#message").show();
      },
      error: function() {
        $("#message").text("Sorry, there was an error. Please check you have uploaded a file that exists and try again.");
        $("#message").show();
      },
    });
   return false;
  });

  $('#query').submit(function(event) {
    event.preventDefault();
    // const values = $(this).serializeArray().reduce(function(obj, item) {
    //     obj[item.name] = item.value;
    //     return obj;
    // }, {});
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
      },
    })
  })

});