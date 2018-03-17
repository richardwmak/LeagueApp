/* jshint node: true */
"use strict";

$(document).ready(function()
{
    $("#submit").on("click", function(event)
    {
        // prevent the button click from automatically reloading
        event.preventDefault();
        submit();
    });
});

function submit(event)
{
    // if the error message is not hidden, hide it
    if (!$("#ajax-error-message").hasClass("hidden"))
    {
        $("#ajax-error-message").hide();
        $("#ajax-error-message").html();
    }

    var username = $("#input-username").val();
    var region = $("#region-select option:selected").val();

    var data = {
        "username": username,
        "region": region
    };

    $.ajax(
        {
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: "POST",
            url: "/set_info",
            data: JSON.stringify(data)
        })
        .done(function(data)
        {
            if (data.success === true)
            {
                window.location.replace("/stats");
            }
            else
            {
                $("#ajax-error-message").html(data.message);
                $("#ajax-error-message").show();
            }
        });
}