"use strict";//more secure js =>error on undeclared variables
(function() {
	var helloApp = angular.module('helloApp');//get module by name
    var helloController = helloApp.controller('FooterHelloController', function($scope) {
    	$scope.message = "footer";
    });
})();