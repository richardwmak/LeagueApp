/* jshint node: true */
"use strict";

$(document).ready(function()
{
    $("#start-btn").on("click", function()
    {
        start($(this));
    });
});

function start(btn)
{
    if(! btn.hasClass("disabled"))
    {
        var circle;
        btn.addClass("disabled");
        btn.children("fa-download").css("background-color", "red");
        // circle = btn.children("fa-circle");
        // circle.removeClass("fa-cirle");
        // circle.addClass("fa-circle-notch");
    }
}