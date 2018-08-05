
var app = angular.module('fakebook', ['ngMaterial', 'ngMessages']);
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});