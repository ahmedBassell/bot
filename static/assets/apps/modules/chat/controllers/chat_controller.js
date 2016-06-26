"use strict";//more secure js =>error on undeclared variables
(function() {
	var chatBot = angular.module('chatBot');//get module by name
    var chatController = chatBot.controller('chatController', ['$scope', '$http', '$timeout',
        function ($scope, $http, $timeout) {
        
        $scope.message = "hello from controller" ;
        $scope.loading = true;
        $scope.input_text = "";
        $scope.base_url = base_url;
        $scope.emo_buffer = "";
        $scope.current_emo = "";
        $scope.session_id = session_id;

        $scope.current_emo = {};
        $scope.current_emo.svm = "NEUTRAL";
        $scope.current_emo.logi = "NEUTRAL";
        $scope.current_emo.multi = "NEUTRAL";

        $scope.emotion = "meh";
        $scope.emotions = []
        $scope.emotions['joy'] = 0;
        $scope.emotions['sadness'] = 0;
        $scope.emotions['shame'] = 0;
        $scope.emotions['disgust'] = 0;
        $scope.emotions['anger'] = 0;
        $scope.emotions['fear'] = 0;

        $scope.emo_drawings = [];
        $scope.emo_drawings['joy']       = 'fa-smile-o';
        $scope.emo_drawings['sadness']   = 'fa-frown-o';
        $scope.emo_drawings['shame']     = 'fa-frown-o';
        $scope.emo_drawings['disgust']   = 'fa-frown-o';
        $scope.emo_drawings['anger']     = 'fa-frown-o';
        $scope.emo_drawings['fear']     = 'fa-meh-o';
        $scope.emo_drawings['meh']       = 'fa-meh-o';
        $scope.emo_drawing =  $scope.emo_drawings['meh'];


        $scope.emo_drawing_colors = [];
        $scope.emo_drawing_colors['joy']       = 'yellow';
        $scope.emo_drawing_colors['sadness']   = 'blue';
        $scope.emo_drawing_colors['shame']     = 'brown';
        $scope.emo_drawing_colors['disgust']   = 'green';
        $scope.emo_drawing_colors['anger']     = 'red';
        $scope.emo_drawing_colors['fear']     = 'violet';
        $scope.emo_drawing_color = "grey";

        // $scope.emotion = "neutral";


        $scope.emo_image_path = static_url+"assets/img/emotions/"+$scope.emotion+'.jpg';



        $scope.classify_emotion = function(){
            $scope.emotions[$scope.current_emo.svm] ++;
            $scope.emotions[$scope.current_emo.logi] ++;
            $scope.emotions[$scope.current_emo.multi] ++;
            var emos = $scope.emotions; 
            console.log(emos);
            // emos.sort();
            // emos.reverse();
            var max_emo = "";
            var max_emo_score = 0;
            for(var i in emos){
                var emo = emos[i];
                if(emo > max_emo_score){
                    max_emo = i;
                    max_emo_score = emo;
                }
            }


            $scope.emotions['joy'] = 0;
            $scope.emotions['sadness'] = 0;
            $scope.emotions['shame'] = 0;
            $scope.emotions['disgust'] = 0;
            $scope.emotions['anger'] = 0;
            $scope.emotions['fear'] = 0;


            return max_emo;
        };
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

        $scope.new_message = function(text, time, sender){
            var message = {}
            message.text = text;
            message.date = time;
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
            

            // GET EMOTION
            $scope.emo_buffer += $scope.input_text;
            $scope.emo_buffer += " ";
            if($scope.emo_buffer.length > 50 ){
            console.log($scope.emo_buffer.length);
                $scope.get_emotion($scope.emo_buffer);
                $scope.emo_buffer = "";
            }







            console.log(Date());
            $scope.new_message($scope.input_text, new Date(), 1);

            // post message
            $scope.send_message($scope.input_text);

            $scope.input_text = "";
            // var elem = document.getElementById('mess');
            // window.scrollTop = 50;

            $(window).scrollTop($(document).height() );
        };

        $scope.send_message = function(msg){
            var data = 
            {
                input: msg,
                session_id : $scope.session_id
            };
            // var data = $.param({
            //     input: msg
            // });
            $http.post(($scope.base_url+"/result"), data)
                .then(function(response) {
                    // console.log(response.data.input);
                    // console.log(response.data.output);
                    var output = response.data.output;
                    $scope.new_message(output, new Date(), 5);
                    // var message = {}
                    // message.text = output;
                    // message.time = "20:11";
                    // message.sender_id = 0;
                    // $scope.messages.push(message);
                });
        };

        $scope.get_old_convs = function(){
            $http.get($scope.base_url+"/chats?sess="+$scope.session_id)
            .then(function(response) {
                var output = response.data;
                $scope.messages = output;
            });

        };

        console.log(session_id);
        $scope.get_emotion = function(emo_buffer){
            var data = 
            {
                input: emo_buffer
            };
            
            $http.post(($scope.base_url+"/emo"), data)
                .then(function(response) {
                    var output = response.data.output;
                    $scope.current_emo = output;
                    $scope.current_emo.svm = output['SVM'];
                    $scope.current_emo.logi = output['Logistic Regression'];
                    $scope.current_emo.multi = output['Multinomial Naive Bayes'];
                    // console.log(output);
                    // $('#myModal').modal({
                    //   keyboard: true
                    // });

                    $scope.adjust_emotion_drawing();
                });
        };

        $scope.adjust_emotion_drawing = function(){
            $scope.emotion = $scope.classify_emotion();
            var final_emo = $scope.emotion;
            console.log($scope.emotion);
            $scope.emo_drawing = $scope.emo_drawings[final_emo];
            $scope.emo_drawing_color = $scope.emo_drawing_colors[final_emo];

            $scope.emo_image_path = static_url+"assets/img/emotions/"+$scope.emotion+'.jpg';
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
