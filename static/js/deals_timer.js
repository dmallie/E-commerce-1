'use strict';
function deadLineTimer(){
       var days_html = document.querySelector("#day");
       var hr_html = document.querySelector("#hour");
       var min_html = document.querySelector("#min");
       var sec_html = document.querySelector("#sec");
       
// var endTime=new Date({{ ob.date|date:"U" }} * 1000)
       var deadLine = new Date("October 25, 2022 14:00:00");
       deadLine = (Date.parse(deadLine)/ 1000);
       
       var now = new Date();
       now = (Date.parse(now)/1000);

       var timeLeft = deadLine - now;

       var days = Math.floor(timeLeft / 86400);
       var hours = Math.floor((timeLeft - (days*86400))/3600);
       var minutes = Math.floor((timeLeft - (days*86400 + hours*3600))/60);
       var seconds = Math.floor((timeLeft - (days*86400 + hours*3600 + minutes*60)));

       if (hours < "10"){
              hours = "0" + hours;
       }
       if(minutes < "10"){
              minutes = "0" + minutes;
       }
       if(seconds < "10"){
              seconds = "0" + seconds
       }

       days_html.textContent       = days;
       hr_html.textContent         = hours;
       min_html.textContent        = minutes;
       sec_html.textContent        = seconds;
       // console.log(sec_html);
       // $("#days").html(days + "<span>Days</span>");
       // $("#hours").html(hours + "<span>Hours</span>");
       // $("#minutes").html(minutes + "<span>Minutes</span>");
       // $("#seconds").html(seconds + "<span>Seconds</span>");
}

setInterval(function() { deadLineTimer(); }, 1000);
