


$(document).ready(function() {
  $("#progress").text("0");

  $("#hidden-invoker").click(function() {
    var progress = $("#progress");
    var currentVal = parseInt(progress.text());
    if (currentVal < 100) {
      updateProgress(progress, currentVal + 10);
    }
  });
});

function updateProgress(progress, newVal) {
  progress.text(newVal);
  $("#element2").width(newVal + "%");


  if (newVal < 100) {
    setTimeout(function() {
      updateProgress(progress, newVal + 10);
    }, 700);
  }
}


$(function() {
  $("#searchForm").submit(function(e) {
     $("#progress").text("0");
    e.preventDefault();
    $("#hidden-invoker").click();
    $("#loading").show();
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
                    $("#progress").text("100");
                    $("#element2").width(100 + "%");
                    $("#loading").hide();
                    
                    if (a["domain"]=="youtube"){
                      $("#iframe").attr('src',a["key"]);
                      let value=`<select id="videores">`;
                      Object.keys(a["data"]["video"]).forEach(function(key) {
                        value = value+`
                      
                          <option value="">${key.substring(1,key.length-1)}</option>
                          `;

                      });
                      value=value+"</select>"
       
                      $("#videores").replaceWith(value);
                      let value2=`<select id="audiores">`;
                      Object.keys(a["data"]["audio"]).forEach(function(key) {
                        value2 = value2+`
                      
                          <option value="">${key}</option>
                          `;

                      });
                      value2=value2+"</select>"
       
                      $("#audiores").replaceWith(value2);             
                    }
                  
                }
                else{
                  $('#info').text("Unrecognised Domain Detected!");
                  $("#info").hide();
                  $("#info").fadeIn("slow");
                  $("#tabs").hide();
                  $("#iframe").hide();
                  $("#download").hide();
                  $("#loading").hide();


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