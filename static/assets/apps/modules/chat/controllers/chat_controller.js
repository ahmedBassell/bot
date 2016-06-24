"use strict";//more secure js =>error on undeclared variables
(function() {
	var chatBot = angular.module('chatBot');//get module by name
    var chatController = chatBot.controller('chatController', ['$scope', '$http', '$timeout',
        function ($scope, $http, $timeout) {
        
        $scope.message = "hello from controller" ;
        $scope.loading = true;
        // $scope.ks = [
        // {'Keyword': 2},
        // {'Keyword': 3}
        // ];
        // console.log($scope.ks);
     //    $scope.getKeywords = function(){
     //        var keywords = $http.get("http://localhost:8000/keywords/?format=json")
     //        .then(function(response) {
     //            $scope.ks = response.data;
     //            console.log($scope.ks);
     //        });
     //    };
    	// $scope.getKeywords();
        
        $scope.messages = [
            {
                "text": "Hi!",
                "time": "20:17",
                "sender_id": 5,

            },
            // {
            //     "text": "hi bro!",
            //     "time": "20:17",
            //     "sender_id": 1,

            // },
            // {
            //     "text": "Hate you!",
            //     "time": "20:17",
            //     "sender_id": 0,

            // },
            // {
            //     "text": "Fuck off!",
            //     "time": "20:17",
            //     "sender_id": 1,

            // },
            // {
            //     "text": "okay!",
            //     "time": "20:17",
            //     "sender_id": 0,

            // }
        ];

        $scope.new_message = function(text, time="00:00", sender=0){
            var message = {}
            message.text = text;
            message.time = time;
            message.sender_id = sender;
            $scope.messages.push(message);
        };
        $scope.doit = function(){
            // console.log($scope.input_text);
            // var message = {}
            // message.text = $scope.input_text;
            // message.time = "20:11";
            // message.sender_id = 1;
            // $scope.messages.push(message);

            $scope.new_message($scope.input_text, "00:00", 1);

            // post message
            $scope.send_message($scope.input_text);

            $scope.input_text = "";
            var elem = document.getElementById('mess');
            window.scrollTop = 50;

            $(window).scrollTop($(document).height() );
        };

        $scope.send_message = function(msg){
            var data = 
            {
                input: msg
            };
            // var data = $.param({
            //     input: msg
            // });
            $http.post(("http://localhost/result"), data)
                .then(function(response) {
                    // console.log(response.data.input);
                    // console.log(response.data.output);
                    var output = response.data.output;
                    $scope.new_message(output, "00:00", 5);
                    // var message = {}
                    // message.text = output;
                    // message.time = "20:11";
                    // message.sender_id = 0;
                    // $scope.messages.push(message);
                });
        };

        $scope.get_old_convs = function(){
            $http.get("http://localhost/chats")
            .then(function(response) {
                var output = response.data;
                $scope.messages = output;
            });

        };
        $scope.init = function(){
            $timeout(negateLoading, 1000);
            console.log('inited');
        }
        function negateLoading(){
            $scope.loading = false;
        }
        $scope.get_old_convs(); 

    }]);
})();
