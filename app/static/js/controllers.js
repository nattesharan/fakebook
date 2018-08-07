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
FakebookController.$inject = ['$scope','socket'];

function FakebookController($scope,socket) {
    var vm = this;
    vm.establishConnection = establishConnection;
    function establishConnection(user_id) {
        var data = { 'user_id': user_id};
        socket.on('connect',function() {
            socket.emit('create_room',data);
        });
        socket.on('disconnect',function() {
            console.log("disconnected");
        });
    }
}

angular.module('fakebook').controller('FindFriendsController', FindFriendsController);
FindFriendsController.$inject = ['$scope','socket'];

function FindFriendsController($scope,socket) {
    var vm = this;
    vm.active = {};
    socket.on('connected_online',function(data) {
        data.users.forEach(user => {
            vm.active[user] = true;
        });
    });
    socket.on('disconnected_offline',function(data) {
        vm.active = {};
        data.users.forEach(user => {
            vm.active[user] = true;
        });
    });
}