"use strict";//more secure js =>error on undeclared variables
(function() {
	var helloApp = angular.module('helloApp');//get module by name
    var helloController = helloApp.controller('BodyHelloController', 
        ['$scope',
        function ($scope) {
    	
        	$scope.slider_images = [
        		{
        			path: base_url+"/assets/img/apps/hello/slider/football-min.jpg"
        		},
        		{
        			path: base_url+"/assets/img/apps/hello/slider/coworking-min.jpg"
        		},
        		{
        			path: base_url+"/assets/img/apps/hello/slider/events-min.jpg"
        		},
        		{
        			path: base_url+"/assets/img/apps/hello/slider/tickets-min.jpg"
        		}
        	];
        	


            $('.simpldon-carousel, #howitworks, #about, #partners').height($(window).height());
            $('#carousel-example').carousel('cycle');
    }]);
})();
