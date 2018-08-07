
var app = angular.module('fakebook', ['ngMaterial', 'ngMessages', 'ui-notification']);
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});