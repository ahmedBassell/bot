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

        // new Morris.Line({
        // // ID of the element in which to draw the chart.
        // element: 'myfirstchart',
        // // Chart data records -- each entry in this array corresponds to a point on
        // // the chart.
        // data: [
        // { year: '2008', value: 20 },
        // { year: '2009', value: 10 },
        // { year: '2010', value: 5 },
        // { year: '2011', value: 5 },
        // { year: '2012', value: 20 }
        // ],
        // // The name of the data record attribute that contains x-values.
        // xkey: 'year',
        // // A list of names of data record attributes that contain y-values.
        // ykeys: ['value'],
        // // Labels for the ykeys -- will be displayed when you hover over the
        // // chart.
        // labels: ['Value']
        // });
        

        $scope.donut = false;
        $scope.emotions_score = {};

        $scope.get_emotions_score = function(){
            $http.get($scope.base_url+"/profile/emotions")
            .then(function(response) {
                var output = response.data[0];
                $scope.emotions_score = output;
                $scope.donut = true;
                $scope.init_donut($scope.emotions_score);
            });

        };

        $scope.init_donut = function(obj){
            new Morris.Donut({
                element: 'myfirstchart',
                data: [
                    {label: "JOY", value: obj['joy_count']},
                    {label: "SADNESS", value: obj['sad_count']},
                    {label: "ANGER", value: obj['ang_count']},
                    {label: "DISGUST", value: obj['dis_count']},
                    {label: "FEAR", value: obj['fea_count']},
                ],
                colors: [
                    '#ffc107',
                    '#311b92',
                    '#f44336',
                    '#8bc34a',
                    '#9c27b0'
                ],
                resize: true
            });
        };


        // INITIALIZE
        
        $scope.get_emotions_score();
        


    }]);
})();
