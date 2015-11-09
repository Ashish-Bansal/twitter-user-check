var app = angular.module('app', ['ngRoute']);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    console.log("App Initialized");
    $locationProvider.html5Mode(true);
    $routeProvider.when('/', {
        templateUrl: '/none.php'
    });
    $routeProvider.when('/search_python/:search_user', {
        templateUrl: function(attrs) {
            return '/python_result.php?search_user=' + attrs.search_user;
        },
        resolve: {
            app: function ($q) {
                var defer = $q.defer();
                defer.resolve();
                return defer.promise;
            }
        }
    });
    $routeProvider.otherwise({
        redirectTo: '/'
    });
}]);

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
