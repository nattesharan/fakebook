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
    vm.unreadNotifCount = 0;
    vm.establishConnection = establishConnection;
    function establishConnection(user_id) {
        var data = { 'user_id': user_id};
        socket.on('connect',function() {
            socket.emit('create_room',data);
        });
        socket.on('disconnect',function() {
            console.log("disconnected");
        });
        socket.on('received_friend_request',function(data) {
            vm.unreadNotifCount += 1;
        });
    }
}

angular.module('fakebook').controller('NotificationController', NotificationController);
NotificationController.$inject = ['socket','$http'];
function NotificationController(socket,$http) {
    var vm = this;
    vm.notifications = {}
    vm.showNotifications = showNotifications;
    function showNotifications(notifications) {
        console.log(notifications);
    }
}
angular.module('fakebook').controller('FindFriendsController', FindFriendsController);
FindFriendsController.$inject = ['$scope','$http','socket','Notification'];

function FindFriendsController($scope,$http,socket,Notification){
    var vm = this;
    vm.active = {};
    vm.addFriend = addFriend;
    function addFriend(person_id) {
        var data = { 'person_id': person_id };
        $http({
            method: 'POST',
            url: '/api/friend-request',
            data: data
        }).then(function result(response) {
            console.log(response.data);
            if(response.data.success) {
                Notification.success({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
            }
            else {
                Notification.error({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
            }
        });
    }
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