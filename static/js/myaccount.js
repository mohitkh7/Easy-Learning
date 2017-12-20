/*
This file contains the JS code for myaccount page

*/


//this function will toggle active class in side menu
$(document).ready(function(){
	var url = window.location;
	$('#side_menu li a').filter(function () {
        return this.href == url;
    }).parent().addClass('active')
});