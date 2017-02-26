var app = angular.module('wander');

app.controller('JoinGroupController', ['$scope','$http', '$state', function($scope, $http, $state){

	$scope.group = {
		groupCode: "",
		dispName: ""
	};

	$scope.join = function() {

	   var options = {};

	   var watchID = navigator.geolocation.getCurrentPosition(onSuccess, onError, options);

	   function onSuccess(position) {

	   		$http({
			  method: 'POST',
			  url: 'http://23.96.125.188:5000/joinGroup/'+$scope.group.groupCode,
			  data: { "dispName" : $scope.group.dispName, "loc" : [position.coords.latitude, position.coords.longitude] }
			}).then(function successCallback(response) {
			    // this callback will be called asynchronously
			    // when the response is available
			    //$rootScope.group = angular.copy($scope.group);
			    console.dir($scope.group);
			    $state.go('joined', { obj : $scope.group });
			  }, function errorCallback(response) {
			    // called asynchronously if an error occurs
			    // or server returns response with an error status.
			    alert("in error");
			  });

	      	console.log('Latitude: '          + position.coords.latitude          + '\n' +
	         'Longitude: '         + position.coords.longitude         + '\n');
	   };

	   function onError(error) {
	      alert('code: '    + error.code    + '\n' +'message: ' + error.message + '\n');
	   }
	}
}]);

app.controller('GroupJoinedController', ['$scope','$http','$state', function($scope, $http, $state){

	$scope.group = $state.params.obj;
	$scope.lost = false;
	//console.dir($scope.group);
	//$scope.group = $rootScope.group;
	$scope.updateLoc = setInterval(function(){ $scope.myTimer(); }, 3000);

	$scope.myTimer = function(){
		var options = {};

	   	var watchID = navigator.geolocation.getCurrentPosition(onSuccess, onError, options);

	   	function onSuccess(position) {
			$http({
				  method: 'POST',
				  url: 'http://23.96.125.188:5000/updateLoc',
				  data: { "groupCode" : $scope.group.groupCode, "dispName" : $scope.group.dispName ,"loc" : [position.coords.latitude, position.coords.longitude] }
				}).then(function successCallback(response) {
				    // this callback will be called asynchronously
				    // when the response is available
				    //console.log(response);
				    if(response.data.lostList.length > 0){
				    	navigator.vibrate(100);
				    	$scope.lost = true;
				    	if(response.data.lostList.length > 2){
				    		$scope.message = response.data.lostList.join(', ') + " are lost";
				    	}
				    	else{
				    		$scope.message = response.data.lostList.join(', ') + " is lost";
				    	}
				    	//alert("Got in!");
				    }
				  }, function errorCallback(response) {
				    // called asynchronously if an error occurs
				    // or server returns response with an error status.
				    //console.log("in error");
				    //console.log(response);
				    clearInterval($scope.updateLoc);
					$state.go('home');
				  });

		      	console.log('Latitude: '          + position.coords.latitude          + '\n' +
		         'Longitude: '         + position.coords.longitude         + '\n');
		   	};

	   function onError(error) {
	      alert('code: '    + error.code    + '\n' +'message: ' + error.message + '\n');
	   }
	}

	$scope.stopUpdateLoc = function(){
		
	}
	
}]);

app.controller('CreateGroupController', ['$scope','$http','$state', function($scope, $http, $state){

	$scope.group = {
		groupName: "",
		dispName: "",
		triggerDist: ""
	}

	$scope.create = function(){

		var options = {};

	   var watchID = navigator.geolocation.getCurrentPosition(onSuccess, onError, options);

	   function onSuccess(position) {

			$http({
			  method: 'POST',
			  url: 'http://23.96.125.188:5000/createGroup',
			  data: {"groupName" : $scope.group.groupName, "dispName" : $scope.group.dispName, "triggerDist" : $scope.group.triggerDist, "loc" : [position.coords.latitude, position.coords.longitude] }
			}).then(function successCallback(response) {
			    // this callback will be called asynchronously
			    // when the response is available
			    console.log("in success");
			    console.log(response.data.groupCode);
			    $scope.group.groupCode = response.data.groupCode;
			    $state.go('created', { obj : $scope.group });
			  }, function errorCallback(response) {
			    // called asynchronously if an error occurs
			    // or server returns response with an error status.
			    alert("in error");
			  });
		};

	   function onError(error) {
	      alert('code: '    + error.code    + '\n' +'message: ' + error.message + '\n');
	   }	
	}

	
}]);

app.controller('EndGroupController', ['$scope','$http','$state', function($scope, $http, $state){

	$scope.group = $state.params.obj;
	$scope.lost = false;

	$scope.updateLoc = setInterval(function(){ $scope.myTimer(); }, 3000);

	$scope.myTimer = function(){
		var options = {};

	   	var watchID = navigator.geolocation.getCurrentPosition(onSuccess, onError, options);

	   	function onSuccess(position) {
			$http({
				  method: 'POST',
				  url: 'http://23.96.125.188:5000/updateLoc',
				  data: { "groupCode" : $scope.group.groupCode, "dispName" : $scope.group.dispName ,"loc" : [position.coords.latitude, position.coords.longitude] }
				}).then(function successCallback(response) {
				    // this callback will be called asynchronously
				    // when the response is available
				    console.log(response);
				    if(response.data.lostList.length > 0){
				    	navigator.vibrate(100);
				    	$scope.lost = true;
				    	if(response.data.lostList.length > 2){
				    		$scope.message = response.data.lostList.join(', ') + " are lost";
				    	}
				    	else{
				    		$scope.message = response.data.lostList.join(', ') + " is lost";
				    	}
				    	//alert("Got in!");
				    }
				  }, function errorCallback(response) {
				    // called asynchronously if an error occurs
				    // or server returns response with an error status.
				    //console.log("in error");
				    //console.log(response);
				  });

		      	console.log('Latitude: '          + position.coords.latitude          + '\n' +
		         'Longitude: '         + position.coords.longitude         + '\n');
		   	};

	   function onError(error) {
	      alert('code: '    + error.code    + '\n' +'message: ' + error.message + '\n');
	   }
	}


	$scope.destroy = function(){

		$http({
		  method: 'GET',
		  url: 'http://23.96.125.188:5000/groupEnd/'+$scope.group.groupCode
		}).then(function successCallback(response) {
		    // this callback will be called asynchronously
		    // when the response is available
		    console.log("in success");
		    clearInterval($scope.updateLoc);
		    $state.go('home');
		  }, function errorCallback(response) {
		    // called asynchronously if an error occurs
		    // or server returns response with an error status.
		    console.log("in error");
		    console.log(response);
		  });
	}
	
}]);