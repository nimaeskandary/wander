// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var app = angular.module('wander', ['ionic']);

app.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  })
});

app.config(function($stateProvider, $urlRouterProvider) {
    //console.log($stateProvider);
    $urlRouterProvider.otherwise("/home");

    $stateProvider
      .state('home', {
        url: "/home",
        templateUrl: "templates/home.html"
      })
      .state('newgroup', {
        url: "/newgroup",
        controller: "CreateGroupController",
        templateUrl: "templates/newgroup.html"
      })
      .state('joingroup',{
        url: "/joingroup",
        controller: "JoinGroupController",
        templateUrl: "templates/joingroup.html"
      })
      .state('joined',{
        url: "/joined",
        controller: "GroupJoinedController",
        params: {
          obj: null
        },
        templateUrl: "templates/group_joined.html"
      })
      .state('created',{
        url: "/created",
        params: {
          obj: null
        },
        controller: "EndGroupController",
        templateUrl: "templates/end_group.html"
      });

  });
