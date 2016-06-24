"use strict";//more secure js =>error on undeclared variables
(function() {
	var helloApp = angular.module('helloApp');//get module by name
    var hiwDirective = helloApp.directive('howItWorks', function() {
    	return{
    		restrict: 'E',
    		templateUrl: base_url+'assets/apps/modules/hello/partials/directives/howitworks.html',
    		controller:"BodyHelloController"
    	}
    });
})();