"use strict";//more secure js =>error on undeclared variables
(function() {
	var helloApp = angular.module('helloApp');//get module by name
    var sliderDirective = helloApp.directive('slider', function() {
    	return{
    		restrict: 'E',
    		templateUrl: base_url+'assets/apps/modules/hello/partials/directives/slider.html',
    		controller:"BodyHelloController",
    		replace: true
    	}
    });
})();