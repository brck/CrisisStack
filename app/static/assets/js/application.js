$(document).ready(function(){
	$('#deleteButton').click(function(){
		$('#deleteButton').html('<i class="fa fa-refresh fa-spin"></i> Deleting');
		var appId = $('#appid').val();
		$.ajax({
			url: '/MyApplications/'+ appId,
			type: 'POST',
		}).then(function (data){
			setTimeout(function(){
				$('#deleteButton').html('<i class="fa fa-tick"></i> Deleted');
			}, 5000);
			window.location.href ="/";
		});
		return false;
	});
});

$(document).ready(function(){
	$('#InstallButton').click(function(){
		$('#InstallButton').html('<i class="fa fa-refresh fa-spin"></i> Installing');
		var appId = $('#appid').val();
		$.ajax({
			url: '/MyApplications/'+ appId,
			type: 'POST',
		}).then(function (data){
			setTimeout(function(){
				$('#InstallButton').html('<i class="fa fa-tick"></i> Installed');
			}, 5000);
			window.location.href ="/";
		});
		return false;
	});
});