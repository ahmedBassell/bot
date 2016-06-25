(function() {
	// identify main module with all dependency modules injected
    var chatBot = angular.module('chatBot', 
    						[
                                'chatApp',
                                'homeApp'
                            ]);

	// changing templating braces cause of laravel conflict
    chatBot.config(function($interpolateProvider){
	    $interpolateProvider.startSymbol('<%').endSymbol('%>');
	});    

    


	

	chatBot.directive('myEnter', function () {
	    return function (scope, element, attrs) {
	        element.bind("keydown keypress", function (event) {
	            if(event.which === 13) {
	                scope.$apply(function (){
	                    scope.$eval(attrs.myEnter);
	                });

	                event.preventDefault();
	            }
	        });
	    };
	});



	chatBot.directive('myTab', function () {
	    return function (scope, element, attrs) {
	        element.bind("keydown keypress", function (event) {
	            if(event.which === 13) {
	                scope.$apply(function (){
	                    scope.$eval(attrs.myEnter);
	                });

	                event.preventDefault();
	            }
	        });
	    };
	});
  	

})();


var myApp = angular.module('myApp',[]);

myApp.controller('GreetingController', ['$scope', function($scope) {
	$scope.greeting = 'Hola!';

}]);





