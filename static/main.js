function triggerPing(){
    var intervalId=window.setInterval(function(){loadnewdata()},1000)
    function loadnewdata(){
      var text=parseInt($("#progress").text());
      $.ajax({
        url:'/return-percentage',
        type:'POST',
        success:function(response){
          
          console.log(response);
          var a = JSON.parse(response);
          var checking = a["percentage"];
          $("#progress2").text(checking);
        
          if (text!=checking){
                $("#progress2").text(checking);
                text=checking;
          }
          if (text==100){
            $("#loader2").hide();
           clearInterval(intervalId);


          }
        }
      });
    }
  };



$(function() {
  $("#myForm2").submit(function(e) {
     $("#progress2").text("0");
        e.preventDefault();
        $("#loader2").show();
        $.ajax({
            url: '/',
            data:$(this).serialize(),
            type: 'POST',
            success: function(response) {
              e.preventDefault();
              const a = JSON.parse(response);
              if (a['status']=='ok'){
                $("#loader2").show();
                triggerPing();

              }
              if (a["status"]=="bad"){
                $('#info').text("Error! Please Select Another.");
                $('#progress2').hide();
                $("#loader2").hide();

              }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


$(function() {
  $("#myForm").submit(function(e) {
     $("#progress").text("0");
    e.preventDefault();
        $.ajax({
            url: '/',
            data:$(this).serialize(),
            type: 'POST',
            success: function(response) {
              e.preventDefault();
              const a = JSON.parse(response);
              if (a['status']=='ok'){
                //invoke ping function here
                  

              }
              if (a["status"]=="bad"){
                $('#info').text("Error! Please Select Another.");
                $('#progress').hide();

              }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});





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
                    $("#prev").text("VIDEO PREVIEW");
                    $("#tabs").hide();
                    $("#tabs").fadeIn("slow");
                    $("#download").show();
                    $("#iframe").hide();
                    $("#iframe").fadeIn("slow");
                    $("#prev").hide();
                    $("#info").hide();
                    $("#prev").fadeIn("slow");
                    $("#download-video").show();
                    $("#detail").show();
                    $("#progress").text("100");
                    $("#element2").width(100 + "%");
                    $("#loading").hide();
                    
                    if (a["domain"]=="youtube"){
                      $("#iframe").attr('src',a["key"]);
                      let value=`<select id="videores" name="videores">`;
                      Object.keys(a["data"]["video"]).forEach(function(key) {
                        value += `<option value="${key.substring(1, key.length-1)}">${key.substring(1, key.length-1)}</option>`;
                      });
                      value=value+"</select>"
       
                      $("#videores").replaceWith(value);
                      let value2=`<select id="audiores" name="audiores">`;
                      Object.keys(a["data"]["audio"]).forEach(function(key) {
                        value2 += `<option value="${key.substring(0, key.length)}">${key.substring(0, key.length)}</option>`;
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
                  $("#prev").hide();


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