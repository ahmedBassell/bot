"use strict";//more secure js =>error on undeclared variables
(function() {
	var homeApp = angular.module('homeApp');//get module by name
    var homeController = homeApp.controller('homeController', ['$scope', '$http', '$timeout',
        function ($scope, $http, $timeout) {

        $scope.loading = true;
        $scope.base_url = base_url;

        $scope.init = function(){
            $timeout(negateLoading, 1000);
            console.log('inited');
        }
        function negateLoading(){
            $scope.loading = false;
        }

    }]);
})();
