/***
 * This is the main JSript file.All events defined her are subject to modification.
 */

// ----------TABS----------- 
function openContent(evt,contentName){
   var i ,tabcontent,tablinks;
   //Get all elements with class "tabcontent " and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for(i = 0;i < tabcontent.length; i++){
      tabcontent[i].style.display = "none";
    }
    //GET all elements with class "tablinks " and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for(i = 0;i < tablinks.length; i++){
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    //Show the current tab, and add an "active" class to the link the opened the tab
    document.getElementById(contentName).style.display = "grid";
    evt.currentTarget.className += " active";
}


/**
 *  THIS FUNCTION Gets the ROUTE INFORMATION IN SECTION PANEL,SUBJECT TO IMPROVEMENT 
 *  Use jQuery .each() method to add an anonymus function which does the job here,
 *  Use jQuery to attch the event rather than the Plain JS methods
 *    Allow for route drawing on clicking the checkbox of the cell element, (as well as removal)
 *    Allow removing the route from the side map by unchecking from the leaflet route control,
 *    The div that displays specific route information can be placed as an element on the map
 *    Allow for search and sort on the table via dates,route names, addresses, drivers
 *    Enable geocoding of the route addresses on the map,
 *    Add icons on the stop geometries to indicate stop locations,
 *    Add different styling for different routes on the side map
 *    Allow for one to one routing on the map
 *    Place a div element on the map that allows live tracking to commence .......
 * 
 *  
 * * */ 


/**
 * 
 * 



function getDisplay(e){
  var target;
  if(!e){
    e = window.event;
  }
  target = e.target || e.srcElement;
  var routeInfo = document.getElementById('sideslide');
  target = document.getElementById('tableBody').querySelectorAll('input[type="checkbox"]');
  for(var g = 0; g < target.length;g ++){
      if(target[g].checked){
        routeInfo.removeAttribute('id');
        routeInfo.className = 'sidepanel';
      }
   }
   if(e.preventDefault){
     e.preventDefault();
   }
   else{
     e.returnValue = false;
   }
}

// Add Event Listener
var elBody = document.getElementById('tableBody');
if(elBody.addEventListener){
  elBody.addEventListener("change",function(e){
    getDisplay(e);
  },true);
}
else{
  elBody.attachEvent("onchange",function(e){
    getDisplay(e);
  });
}

//THIS FUNCTION Closes the section Panel THAT Displays the route INFORMATION,SUBJECT TO IMPROVEMENT
function closePanel(e){
  var target;
  var panel; 
  if(!e){
    e = window.event;
  }
  target = e.target || e.srcElement;
  panel=document.querySelector('section.sidepanel');
  panel.id = 'sideslide';
}

// ADD EVENT LISTENER
var closeMark = document.getElementById('closebutton');
if(closeMark.addEventListener){
  closeMark.addEventListener("click",function(e){
    closePanel(e);
  },false);
}
else {
  closeMark.attachEvent("click",function(e){
    closePanel(e);
  })
}

 * 
 * 
 */



