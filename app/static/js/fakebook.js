
var app = angular.module('fakebook', ["ngRoute"]);
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "../../../fakebook/templates/dashboard.html"
    });
});