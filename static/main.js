//const { replaceWith } = require("cheerio/lib/api/manipulation");

$(function() {
  $("#searchForm").submit(function(e) {
    e.preventDefault();
        $.ajax({
            url: '/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
              const a = JSON.parse(response);
                if (a["status"]=="ok"){
                    $("#info").text("VIDEO PREVIEW");
                    $("#tabs").hide();
                    $("#tabs").fadeIn("slow");
                    $("#download").show();
                    $("#iframe").hide();
                    $("#iframe").fadeIn("slow");
                    $("#info").hide();
                    $("#info").fadeIn("slow");
                    $("#download-video").show();
                    $("#detail").show();
                    if (a["domain"]=="youtube"){
                      $("#iframe").attr('src',a["key"]);
                    }
                  
                }
                else{
                  $('#info').text("Unrecognised Domain Detected!");
                  $("#info").hide();
                  $("#info").fadeIn("slow");
                  $("#tabs").hide();
                  $("#iframe").hide();
                  $("#download").hide();


                }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


function download(){
    document.getElementById("download").style.display="inherit";
}
function navi(){
    var navi=document.getElementById("nav-item");
    if(navi.style.height==="0%"){
        navi.style.height="30%"
    }
    else{
       navi.style.height="0%";
    }
}

function tabs(evt,tabName) {
    var i, tabcontent, tablinks;
  
    tabcontent = document.getElementsByClassName("videoandaudio");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    tablinks = document.getElementsByClassName("button2");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].style.backgroundColor="transparent";
      tablinks[i].style.color="grey";
    }
  
    document.getElementById(tabName).style.display = "block";
    tablinks[evt].style.backgroundColor="rgb(255, 60, 0)";
    tablinks[evt].style.color="white";
  } 