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

angular.module('fakebook').controller('NotificationController', NotificationController);
NotificationController.$inject = ['socket','$http'];
function NotificationController(socket,$http) {
    var vm = this;
    vm.unreadNotifCount = 0;
    vm.notifications = []
    vm.fetchNotifications = fetchNotifications;
    vm.notificationsOpened = notificationsOpened;

    function notificationsOpened() {
        $http({
            method: 'PUT',
            url: '/api/notifications',
            data: {
                'read_notifications': vm.notifications
            }
        }).then(function result(response) {
            vm.unreadNotifCount = 0;
            vm.notifications = response.data.notifications;
            vm.notifications.forEach(notification => {
                if(!notification.is_read) {
                    vm.unreadNotifCount += 1;
                }
            });
        });
    }
    function fetchNotifications() {
        $http({
            method: 'GET',
            url: '/api/notifications'
        }).then(function result(response) {
            vm.notifications = response.data.notifications;
            vm.notifications.forEach(notification => {
                if(!notification.is_read) {
                    vm.unreadNotifCount += 1;
                }
            });
        });
    }
    
    socket.on('received_friend_request',function(data) {
        vm.unreadNotifCount = 0;
        vm.notifications = data;
        console.log(vm.notifications);
        vm.notifications.forEach(notification => {
            if(!notification.is_read) {
                vm.unreadNotifCount += 1;
            }
        });
    });
}
angular.module('fakebook').controller('FindFriendsController', FindFriendsController);
FindFriendsController.$inject = ['$http','socket','Notification','$mdDialog'];

function FindFriendsController($http,socket,Notification,$mdDialog){
    var vm = this;
    vm.active = {};
    vm.people = [];
    vm.addFriend = addFriend;
    vm.acceptRequest = acceptRequest;
    vm.cancelRequest = cancelRequest;
    vm.fetchFriends = fetchFriends;
    vm.confirmUnfriend = confirmUnfriend;

    function confirmUnfriend(event,person_id,person_name) {
        var confirm = $mdDialog.confirm()
          .title(`Would you really want to unfriend ${person_name}?`)
          .textContent('This action cannot be reverted.')
          .ariaLabel('confirmUnfriend')
          .targetEvent(event)
          .ok('Unfriend')
          .cancel('Cancel');

        $mdDialog.show(confirm).then(function() {
            $http({
                method: 'PUT',
                url: '/api/friends',
                data: {
                    'person_id': person_id
                }
            }).then(function result(response) {
                if(response.data.success) {
                    vm.people = response.data.friends;
                    Notification.success({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
                }
                else {
                    Notification.error({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
                }
            });
        });
    }
    function fetchFriends() {
        $http({
            method: 'GET',
            url: '/api/friends'
        }).then(function result(response) {
            vm.people = response.data.friends;
        });
    }
    function addFriend(person_id) {
        var data = { 'person_id': person_id };
        $http({
            method: 'POST',
            url: '/api/friend-request',
            data: data
        }).then(function result(response) {
            if(response.data.success) {
                vm.people = response.data.friends;
                Notification.success({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
            }
            else {
                Notification.error({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
            }
        });
    }

    function acceptRequest(person_id) {
        $http({
            method: 'PUT',
            url: '/api/friend-request',
            data: {
                'person_id': person_id
            }
        }).then(function result(response) {
            if(response.data.success) {
                Notification.success({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
                fetchFriends();
            }
            else {
                Notification.error({message: response.data.message, delay: 1000, positionY: 'bottom', positionX: 'right'});
            }
        });
    }

    function cancelRequest(person_id) {
        $http({
            method: 'DELETE',
            url: '/api/friend-request',
            params: {
                'person_id': person_id
            }
        }).then(function result(response) {
            if(response.data.success) {
                vm.people = response.data.friends;
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
    
    socket.on('update_people_list',function() {
        fetchFriends();
    });
    
    socket.on('disconnected_offline',function(data) {
        vm.active = {};
        data.users.forEach(user => {
            vm.active[user] = true;
        });
    });
}

angular.module('fakebook').controller('UserNotificationsController', UserNotificationsController);
UserNotificationsController.$inject = ['$http','socket'];

function UserNotificationsController($http,socket) {
    var vm = this;
    vm.notifications = [];
    vm.loadNextPageNotifications = loadNextPageNotifications;
    vm.endOfPage = false;
    vm.busy = false;
    vm.limit = 10;
    vm.skip = 0;
    function loadNextPageNotifications() {
        vm.busy = true;
        $http({
            method: 'GET',
            url: '/api/user/notifications',
            params: {
                'skip': vm.skip,
                'limit': vm.limit
            }
        }).then(function result(response) {
            vm.busy = false;
            console.log(response.data.notifications);
            response.data.notifications.forEach(notification => {
                vm.notifications.push(notification);
            });
            if(response.data.notifications.length < vm.limit) {
                vm.endOfPage = true;
            }
            vm.skip += vm.limit;
        });
    }
}