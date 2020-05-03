
$(document).ready(function() {
    $('.submit').click(function(){  
        // display loading spinner
        $(".results").hide();
        $(".loading").show();

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
                $('.drum-link').replaceWith(`<a href="${data.drum_link}">drum link</a>`);
                $('.audio-link').replaceWith(`<a href="${data.audio_link}">audio link</a>`);
            },
            error: function(error){
                console.log(error);
                $(".loading").hide();
            }
        });
    });
});
