"use strict";//more secure js =>error on undeclared variables
(function() {
var helloApp = angular.module('helloApp');//get module by name
helloApp.directive("scroll", function ($window) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
                var container = $('#'+attrs.id);
                container.on("scroll", function() {
                     if (container.scrollTop() >= 200) {
                         scope.navChange = true;
                     } else {
                         scope.navChange = false;
                     }
                    scope.$apply();
                });
            }
    }
});
})();