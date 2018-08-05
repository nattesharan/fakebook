
var app = angular.module('fakebook', ["ngRoute"]);
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});