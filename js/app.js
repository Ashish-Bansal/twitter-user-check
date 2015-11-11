var app = angular.module('app', ['ngRoute']);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    console.log("App Initialized");
    $locationProvider.html5Mode(true);
    $routeProvider.when('/', {
        templateUrl: '/none.php'
    });
    $routeProvider.when('/search_python/:search_user', {
        templateUrl: '/result_template.html',
        controller: 'JudgementResult'
    });
    $routeProvider.otherwise({
        redirectTo: '/'
    });
}]);

app.run(function ($templateCache, $http) {
    $http.get('/result_template.html', { cache: $templateCache });
});

app.controller('FormController', ['$scope', '$location', function($scope, $location) {
    $scope.submit = function() {
        if ($scope.search_user) {
            console.log("/python_result.php?search_user="+$scope.search_user);
            $location.path("/search_python/"+$scope.search_user);
        }
    };
}]);

app.controller('ViewController', ['$scope', '$location', function($scope, $location) {
    $scope.$on('$viewContentLoaded', function(){
        console.log("View Content loaded");
    });
}]);

app.controller('JudgementResult', ['$scope', '$routeParams', '$http', function($scope, $routeParams, $http) {
    $scope.fetched = false;
    var judgeUrl = "/python_result.php/?search_user=".concat($routeParams.search_user);
    $http.get(judgeUrl)
    .success(function(data, status, headers, config) {
        console.log("Result fetched");
        $scope.fetched = true;
        $scope.result = data;
        console.log(data);
    })
    .error(function(data, status, headers, config) {
        console.log("Error fetching Result!");
    });
}]);
