$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#dismiss, .overlay').on('click', function () {
        saveConfigurationAndClose();
    });

    $('#model_name, #api_key').on('change', function() {
        sessionStorage.setItem(this.id, this.value);
    });

    $('#sidebarCollapse').on('click', function () {
        // open sidebar
        $('#sidebar').addClass('active');
        // fade in the overlay
        $('.overlay').addClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');

        // Load the stored values when the sidebar is opened
        if (sessionStorage.getItem('model_name')) {
            $('#model_name').val(sessionStorage.getItem('model_name'));
        }
        if (sessionStorage.getItem('api_key')) {
            $('#api_key').val(sessionStorage.getItem('api_key'));
        }
    });

    $('#saveConfig').on('click', function() {
        saveConfigurationAndClose();
    });

});

function saveConfigurationAndClose() {
    var modelName = $('#model_name').val();
    var apiKey = $('#api_key').val();

    $.post('/update-config', { model_name: modelName, api_key: apiKey })
     .done(function() {
         $('#sidebar').removeClass('active');
         $('.overlay').removeClass('active');
     })
     .fail(function(error) {
         console.error("Error saving configuration: ", error);
     });
}

function adjustSidebar() {
    var headerHeight = $('.navbar').outerHeight(); 
    $('#sidebar').css('margin-top', headerHeight + 'px'); 
}

// Adjust the sidebar on page load
$(document).ready(adjustSidebar);

// Adjust the sidebar on window resize
$(window).resize(adjustSidebar);