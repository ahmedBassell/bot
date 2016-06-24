"use strict";//more secure js =>error on undeclared variables
(function() {
	var helloApp = angular.module('helloApp');//get module by name
    var helloController = helloApp.controller('HeaderHelloController',
	    ['$scope', '$anchorScroll', '$location',
        function ($scope, $anchorScroll, $location) {
	    	$scope.message = "header";
	    	$scope.base_url = base_url;


	    	$scope.gotoAnchor = function(x) {
	            var newHash =  x;
	            console.log(x);
	            if ($location.hash() !== newHash) {
	            // set the $location.hash to `newHash` and
	            // $anchorScroll will automatically scroll to it
	            $location.hash('anchor' + x);
	            } else {
	            // call $anchorScroll() explicitly,
	            // since $location.hash hasn't changed
	            $anchorScroll();
	            }
	        };
    }]);
})();