angular.module('fakebook').controller('DashboardController', DashboardController);

DashboardController.$inject = ['$scope'];

function DashboardController($scope) {
    var vm = this;
    vm.test = test;
    function test() {
        console.log("it worked");
    }
}

angular.module('fakebook').controller('FakebookController', FakebookController);
FakebookController.$inject = ['$scope','socket']

function FakebookController($scope,socket) {
    var vm = this;
    vm.test = test;
    function test() {
        socket.on('connect',function() {
            console.log('Successfully connected to socket');
        });
    }
}