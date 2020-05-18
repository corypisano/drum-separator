
$(document).ready(function() {

    $('.submit').click(function(){  
        // display loading spinner
        $(".results").hide();
        $(".loading").show();
        $('#break-up-btn').prop('disabled', true);


        // can't pass Jquery form, has to be javascript form object
        var form = $("form");
        var formData = new FormData(form[0]);
        
        var url = "/process";
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                console.log(data);
                $(".loading").hide();    
                $(".results").show();
                $('#break-up-btn').prop('disabled', false);
                $(".error").hide();
                $('.drum-link').attr("href", data.drum_link);
                $('.audio-link').attr("href", data.audio_link);
            },
            error: function(error){
                console.log(error);
                $(".loading").hide();
                $(".error").show();
                $('#break-up-btn').prop('disabled', false);
                $(`<p>Oops, there was an error: ${error.statusText}</p>`).appendTo('.error');
            }
        });
    });
});
