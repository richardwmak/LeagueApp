/* jshint node: true */
"use strict";

var currently_downloading = false;

$(document).ready(function()
{
    var start_btn;
    var start_btn_circle;
    var pause_btn;
    var pause_btn_circle;

    start_btn = $("#start-btn");
    start_btn_circle = $("#start-btn-circle");
    pause_btn = $("#pause-btn");
    pause_btn_circle = $("#pause-btn-circle");

    start_btn.on("click", function()
    {
        start(start_btn, start_btn_circle, pause_btn, pause_btn_circle);
    });

    pause_btn.on("click", function()
    {
        pause(start_btn, start_btn_circle, pause_btn, pause_btn_circle);
    });
});

function start(start_btn, start_btn_circle, pause_btn, pause_btn_circle)
{
    start_btn.prop("disabled", true);
    pause_btn.prop("disabled", false);
    start_btn_circle.toggleClass("fa fa-circle-notch fa-spin far far-circle");
    if (pause_btn_circle.hasClass("fa-spin"))
    {
        pause_btn_circle.toggleClass("fa fa-circle-notch fa-spin far far-circle");
    }

    $.ajax(
    {
        type: "POST",
        url: "/ajax/listen_history_download"
    }).done(function(data)
    {
        if (data.success === true)
        {
            currently_downloading = true;
        }
    });
}

function pause(start_btn, start_btn_circle, pause_btn, pause_btn_circle)
{
    start_btn.prop("disabled", false);
    pause_btn.prop("disabled", true);
    start_btn_circle.toggleClass("fa fa-circle-notch fa-spin far far-circle");
    pause_btn_circle.toggleClass("fa fa-circle-notch fa-spin far far-circle");

    pause_download();
}

function pause_download()
{
    $.ajax(
    {
        type: "POST",
        url: "/ajax/listen_history_pause"
    }).done(function(data)
    {
        if (data.success === true)
        {
            currently_downloading = false;
        }
    });
}

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/round
function precision_round(number, precision)
{
    var factor = Math.pow(10, precision);
    return Math.round(number * factor) / factor;
}

function check_progress()
{
    if (currently_downloading === true)
    {
        $.ajax(
        {
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: "POST",
            url: "/ajax/listen_history_progress"
        }).done(function(data)
        {
            console.log(data);
            var progress = precision_round(100 * (data.current_page / data.total_pages), 2) + "%";
            $("#progress-bar").css("width", "calc(" + progress + " - 0.2rem)");
            $("#progress-bar").html(progress);

            // fallback in case python fails
            if (data.current_page >= data.total_pages)
            {
                pause_download();
                window.location.replace("/stats");
            }
        });
    }

    setTimeout(check_progress, 2000);
}

check_progress();