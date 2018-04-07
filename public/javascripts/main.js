(function() {
    'use strict';
    angular.module('myApp', [])
        .controller('myCtrl1', myCtrlFn)
        .service('myService1', myServiceFn)
        .directive('myList', myListDir);
    //    .constant('ApiBasePath', "http://localhost:3000");

    myListDir.$inject = [];

    function myListDir() {
        var ddo = {
            templateUrl: 'listItem.html',
            scope: {
                listCtrl: "=list"
            },
            //link: myLinkFn
        }
        return ddo;
    }

    function myLinkFn(scope, element, attrs, controller) {
        scope.$watch('listCtrl.itemList', function(newValue, oldValue) {
            console.log(newValue + " :: " + oldValue);

            element.find(".dontshow").html("Hello");
            element.find(".dontshow").slideUp(2000);
            //element.fadeIn(5000);
        })
    }
    myCtrlFn.$inject = ['$scope', '$interval', 'myService1'];


    function myCtrlFn($scope, $interval, myService1) {
        var c1 = this;

        c1.populateTable = function(indate) {
            // console.log("Initiate data retrieval " + indate);
            var promise = myService1.getData(indate);
            promise.then(function(response) {
                var valueArray1 = [];
                var valueArray2 = [];
                var valueArray3 = [];
                var valueArray4 = [];
                var valueArray5 = [];
                var valueArray6 = [];
                var valueArray7 = [];

                for (var i = 0; i < response.data.length; i++) {
                    valueArray1.push(response.data[i].close[0].value)
                    valueArray2.push(response.data[i].close[1].value)
                    valueArray3.push(response.data[i].close[2].value)
                    valueArray4.push(response.data[i].close[3].value)
                    valueArray5.push(response.data[i].close[4].value)
                    valueArray6.push(response.data[i].close[5].value)
                    valueArray7.push(response.data[i].close[6].value)
                }
                c1.indexes.data = [];
                var obj = {};
                obj[response.data[0].close[0].stock] = valueArray1;
                c1.indexes.data.push(obj);
                // c1.indexes.data[0][response.data[0].close[0].stock] = valueArray1;
                obj = {};
                obj[response.data[0].close[1].stock] = valueArray2;
                c1.indexes.data.push(obj);
                obj = {};
                obj[response.data[0].close[2].stock] = valueArray3;
                c1.indexes.data.push(obj);
                obj = {};
                obj[response.data[0].close[3].stock] = valueArray4;
                c1.indexes.data.push(obj);
                obj = {};
                obj[response.data[0].close[4].stock] = valueArray5;
                c1.indexes.data.push(obj);
                obj = {};
                obj[response.data[0].close[5].stock] = valueArray6;
                c1.indexes.data.push(obj);
                obj = {};
                obj[response.data[0].close[6].stock] = valueArray7;
                c1.indexes.data.push(obj);
                c1.indexes.date = response.data[0].date;

                // console.log("Date: " + response.data[0].date + " : " + response.data[1].date + " : " + response.data[2].date);
            })
            .catch(function(error) {
                console.log("Error getCount"+error);
            });
        };

        $scope.getIndex = function(caseNo) {
            console.log("clicked");
            c1.joe = 'jos-' + caseNo;
            switch(caseNo){
                case 1: //c1.indexes.ldate = new Date("2012-08-19");
                        c1.populateTable("2012-08-19");
                        break;
                case 2: //c1.indexes.ldate = new Date("2008-12-11");
                        c1.populateTable("2008-12-11");
                        break;
                case 3: //c1.indexes.ldate = new Date("2000-01-25");
                        c1.populateTable("2000-01-25");
                        break;
            }
        }

        $scope.trunc = Math.trunc;
        $scope.compare = function(val1, val2) {
            if (val1 > val2) return true;
            else return false;
        }
        c1.indexes = {};
        c1.indexes.data = [];
        c1.indexes.ldate = new Date();

        var options = {
            year: "numeric", month: "short",
            day: "numeric", hour: "2-digit", minute: "2-digit"
        };

        function formatDate(date) {
            var d = new Date(date),
                month = '' + (d.getMonth() + 1),
                day = '' + d.getDate(),
                year = d.getFullYear();

            if (month.length < 2) month = '0' + month;
            if (day.length < 2) day = '0' + day;

            return [year, month, day].join('-');
        }

        // c1.indexes.ldate = new Date(c1.indexes.date)
        $scope.$watch('c1.indexes.ldate', function(newValue, oldValue) {
            if (oldValue != newValue) {
                c1.indexes.date = new Date(newValue).toLocaleDateString("en-US")
                // console.log(c1.indexes.date);
                var modDate = formatDate(new Date(newValue));
                c1.populateTable(modDate);
            }
        });

        c1.tooltiptext = "Predict the price movement";
        $scope.isDisabled = false;
        $scope.searchButtonText = "";

        $scope.toggleButton = function() {
            if($scope.searchButtonText == "") {
                $scope.searchButtonText = "searching"
                c1.tooltiptext = "Cancel the prediction";
                // angular.element.find('[data-toggle="tooltip"]')[0].tooltip();
                // angular.element.find('#date-input')[0].focus();
                angular.element.find('[data-toggle="tooltip"]')[0].dataset.originalTitle = "Cancel the prediction";

            } else {
                $scope.searchButtonText = ""
                c1.tooltiptext = "Predict the price movement";
                angular.element.find('[data-toggle="tooltip"]')[0].dataset.originalTitle = "Predict the price movement";
                // $('[data-toggle="tooltip"]').tooltip()
            }
        }
        c1.count = {};
        c1.imagedata = {};

    };

    // myServiceFn.$inject = ['$http', 'ApiBasePath'];
    //
    // function myServiceFn($http, ApiBasePath) {

    myServiceFn.$inject = ['$http'];
    function myServiceFn($http) {
        var mySer = this;
        mySer.getData = function(indate) {
            var response = $http({
                method: "GET",
                url: "/fin/" + indate
                //url: ApiBasePath + "/data"
            });
            return response;
        }

    }

})();
