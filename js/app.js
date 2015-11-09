var app = angular.module('app', ['ngRoute']);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    console.log("App Initialized");
    $locationProvider.html5Mode(true);
    $routeProvider.when('/', {
        templateUrl: '//none.php'
    });
    $routeProvider.when('/search_python', {
        templateUrl: '//python_result.php'
    });
    $routeProvider.otherwise({
        redirectTo: '/'
    });
}]);
