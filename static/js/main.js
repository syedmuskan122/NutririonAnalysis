$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict button click
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        var apiUrl = '/predict'; // default (if HTML is served by Flask)

        // If HTML runs separately (e.g., Live Server port 5500), use full Flask URL:
        if (window.location.port !== "5000") {
            apiUrl = 'http://127.0.0.1:5000/predict';
        }

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        $.ajax({
            type: 'POST',
            url: apiUrl,
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);

                // If Flask returned JSON
                if (data.prediction) {
                    $('#result').html("<b>Food Classified is:</b> " + data.prediction.toUpperCase());
                } 
                // If Flask returned plain text
                else {
                    $('#result').html(data);
                }

                console.log('✅ Prediction success!');
            },
            error: function (xhr, status, error) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html("<span style='color:red;'>⚠️ API not responding. Check if Flask server is running.</span>");
                console.error('❌ Error:', error);
            }
        });
    });
});
